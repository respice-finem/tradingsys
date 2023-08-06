import io
import json
import time
import logging

from dataacq.utils.sql_utils.sql_utils import SQLUtils
from dataacq.utils.scraper.apiScraper import APIScraper
from dataacq.utils.s3.s3_utils import S3Utils
from dataacq.sec_master.const import BUCKET_NAME,\
    SEC_MASTER_FILE_NAME, SEC_MASTER_EXCH_MAP,\
    SQL_CREDENTIALS, EODHD_SEARCH_API,\
    EODHD_API_KEY

class SecurityMaster:

    """
    This class does the following:

    1. Parse our security master file
    2. Write to the database
    """

    def __init__(self):
        """Instantiate class."""
        self.s3_client = S3Utils(
            BUCKET_NAME
        )
        self.sql_client = SQLUtils(
            **SQL_CREDENTIALS
        )

    def enrich(
        self,
        ticker: str
    ):
        """
        Enrich our FINRA CAT dataset with ISIN data

        Arguments:
            ticker: Ticker code of security
        Returns:
            isin: ISIN code of ticker
            name: Full name of the ticker
            sec_type: Security Type i.e. Common Stock
        """
        time.sleep(0.07)
        api_link_w_ticker = f"{EODHD_SEARCH_API}{ticker}?api_token={EODHD_API_KEY}&exchange=US&limit=1"
        api_scraper = APIScraper(
            api_link_w_ticker
        )
        response = json.loads(api_scraper.request().decode('UTF-8'))[0]

        return response['ISIN'], response['Name'], response['Type']

    def full_enrich(
        self,
        file_content: bytes
    ) -> dict:
        """
        Parse and enrich our file to be written to database.

        Arguments:
            file_content: File content in bytes format
        Returns:
            security_master_dict: Dictionary of our master security list
        """
        security_master_dict = {}
        file_content_arr = io.BytesIO(file_content).readlines()
        headers = file_content_arr[0].decode('UTF-8').strip().split('|')
        counter = 0
        for rows in file_content_arr[1:]:
            rows_decoded = rows.decode('UTF-8').strip().split('|')
            if len(rows_decoded) == 4 and rows_decoded[-1] == 'N' and\
                rows_decoded[-2] in ('A', 'N', 'P', 'Q'):
                try:
                    security_master_dict[counter] = {
                        headers[i]: rows_decoded[i] for i in range(len(headers)-1)
                    }
                    print(security_master_dict[counter]['symbol'])
                    security_master_dict[counter]['listingExchange'] = SEC_MASTER_EXCH_MAP.get(
                        security_master_dict[counter]['listingExchange']
                    )
                    isin, name, sec_type = self.enrich(
                        security_master_dict[counter]['symbol']
                    )
                    security_master_dict[counter]['ISIN'] = isin
                    security_master_dict[counter]['issueName'] = name
                    security_master_dict[counter]['securityType'] = sec_type
                    security_master_dict[counter]['country'] = 'US'
                    counter += 1
                except:
                    continue
        with open('sec_master.json', 'w') as f:
            f.write(json.dumps(security_master_dict))
        return security_master_dict
    
    def process(
        self
    ):
        """
        Process file and write to DB.
        """
        response_content = self.s3_client.read(
            SEC_MASTER_FILE_NAME
        )['Body'].read()
        security_master_dict = self.full_enrich(response_content)
        # security_master_dict = json.load(open('sec_master.json'))
        query = '''
        INSERT INTO sec_master.master ("isin", "ticker", "exchange", "fullName", "country", "sec_type")
        VALUES %s
        ON CONFLICT ("isin") DO UPDATE SET
        ("ticker", "exchange", "fullName", "country", "sec_type")
        = ("excluded"."ticker", "excluded"."exchange", "excluded"."fullName", "excluded"."country", "excluded"."sec_type");
        '''
        dedupe = ['US72815G1085', 'US94987B1052', 'US4642886208', 'US30040W1080', 
                  'NL0010556684', 'US00162Q1067', 'US42722X1063', 'US65249B1098', 'BE0974358906', 'US8334451098']
        data = [(
            v['ISIN'],
            v['symbol'],
            v['listingExchange'],
            v['issueName'].strip(),
            v['country'],
            v['securityType']
            ) for _,v in security_master_dict.items() if v['ISIN'] is not None and v['ISIN'] not in dedupe]
        _ = self.sql_client.query(query, data, 'write')
