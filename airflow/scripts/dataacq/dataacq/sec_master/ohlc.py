
from dataacq.dataacq.utils.sql_utils.sql_utils import SQLUtils
from dataacq.dataacq.utils.scraper.apiScraper import APIScraper
from dataacq.dataacq.utils.s3.s3_utils import S3Utils
from dataacq.sec_master.const import BUCKET_NAME,\
    SQL_CREDENTIALS, EODHD_SEARCH_API,\
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
        read_query = '''
        SELECT * FROM sec_master.master
        AS m
        WHERE m.sec_type = 'Common Stock'
        
        '''
        return

    def process(self):
        """Process the information."""
        pass
