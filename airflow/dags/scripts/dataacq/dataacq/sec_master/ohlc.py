import json
from datetime import datetime

from scripts.dataacq.dataacq.utils.sql_utils.sql_utils import SQLUtils
from scripts.dataacq.dataacq.utils.scraper.apiScraper import APIScraper
from scripts.dataacq.dataacq.utils.s3.s3_utils import S3Utils
from scripts.dataacq.dataacq.sec_master.const import BUCKET_NAME,\
    SQL_CREDENTIALS, EODHD_EOD_API,\
    EODHD_API_KEY

class OHLC:

    def __init__(self):
        """Instantiate OHLC scraper."""
        self.s3_client = S3Utils(
            BUCKET_NAME
        )
        self.sql_client = SQLUtils(
            **SQL_CREDENTIALS
        )

    def get_tickers(self):
        """Read from master table."""

        query = '''
        SELECT * FROM sec_master.master
        AS m
        WHERE m.sec_type in ('Common Stock', 'ETF')
        '''

        response = self.sql_client.query(query, qtype='read')
        ticker_dict = {
            e[0]: '.'.join([e[1], 'US']) for e in response # TODO: Refactor to handle different countries
        }
        return ticker_dict
    
    def get_data(
        self,
        isin: str,
        ticker: str,
        start_date: str,
        end_date: str
    ):
        """
        Get OHLCV data for a single ticker

        Arguments:
            isin: ISIN of the security
            ticker: Security symbol
            start_date: In %Y-%m-%d format
            end_date: In %Y-%m-%d format
        Returns:
            ohlcv_data: OHLCV values for ticker between the start and end date
        """
        api_link_w_ticker = f"{EODHD_EOD_API}{ticker}?from={start_date}&to={end_date}&fmt=json&&api_token={EODHD_API_KEY}"
        api_scraper = APIScraper(
            api_link_w_ticker
        )
        # datetime.strptime(data['date'], '%Y-%m-%d').date()
        response = json.loads(api_scraper.request().decode('UTF-8'))
        print(response)
        ohlcv_data = [
            (isin, data['open'], data['high'], data['low'], data['close'],
             data['adjusted_close'], data['volume'], data['date'])
            for data in response
        ]
        return ohlcv_data
        

    def bulk_get_data(
        self,
        full_ticker_dict: dict,
        start_date: str,
        end_date: str
    ):
        """

        Arguments:
            full_ticker_dict: Dictionary of ISIN keys and ticker values
            start_date: In %Y-%m-%d format
            end_date: In %Y-%m-%d format
        Returns:
            full_ohlcv_data: List of tuples of OHLCV values
        """
        full_ohlcv_data = []
        for isin, ticker in full_ticker_dict.items():
            ohlcv_data = self.get_data(
                isin,
                ticker,
                start_date,
                end_date
            )
            full_ohlcv_data += ohlcv_data
        return full_ohlcv_data

    def process(
        self,
        start_date: str,
        end_date: str
    ):
        """Process the information."""
        full_ticker_dict = self.get_tickers()
        full_ohlcv_data = self.bulk_get_data(
            full_ticker_dict,
            start_date,
            end_date
        )
        query = '''
        INSERT INTO sec_master.ohlc_eod ("isin", "open", "high", "low", "close", "adj_close", "volume", "date")
        VALUES %s
        ON CONFLICT ("isin", "date") DO UPDATE SET
        ("open", "high", "low", "close", "adj_close", "volume")
        = ("excluded"."open", "excluded"."high", "excluded"."low", "excluded"."close", "excluded"."adj_close", "excluded"."volume");
        '''
        _ = self.sql_client.query(query, full_ohlcv_data, 'write')
        return full_ohlcv_data

# ohlc_obj = OHLC()
# print(ohlc_obj.process(
#     "2023-08-10",
#     "2023-08-11"
# )[:5])
# print(ohlc_obj.get_data(
#     "dummy",
#     "MSFT.US",
#     "2023-08-10",
#     "2023-08-11"
# ))