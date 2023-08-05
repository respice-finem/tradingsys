import io
import json

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

    def isin_enrich(
        self,
        ticker: str
    ):
        """
        Enrich our FINRA CAT dataset with ISIN data

        Arguments:
            ticker: Ticker code of security
        Returns:
            isin: ISIN code of ticker
        """
        api_link_w_ticker = f"{EODHD_SEARCH_API}{ticker}?api_token={EODHD_API_KEY}&exchange=US&limit=1"
        api_scraper = APIScraper(
            api_link_w_ticker
        )
        isin = json.loads(api_scraper.request())[0]['ISIN']
        return isin

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
                security_master_dict[counter] = {
                    headers[i]: rows_decoded[i] for i in range(len(headers)-1)
                }
                security_master_dict[counter]['listingExchange'] = SEC_MASTER_EXCH_MAP.get(
                    security_master_dict[counter]['listingExchange']
                )
                security_master_dict[counter]['ISIN'] = self.isin_enrich(
                    rows_decoded
                )
                counter += 1
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
        security_master_dict = self.enrich(response_content)
        
        _ = self.sql_client.query(query, False)

sm = SecurityMaster()
print(sm.isin_enrich("SPY"))