
from dataacq.utils.sql_utils.sql_utils import SQLUtils
from dataacq.utils.scraper.apiScraper import APIScraper
from dataacq.utils.s3.s3_utils import S3Utils
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

    def process(self):
        """Process the information."""
        pass
