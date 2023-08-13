from dataacq.dataacq.utils.sql_utils.sql_utils import SQLUtils
from dataacq.dataacq.utils.scraper.apiScraper import APIScraper
from dataacq.dataacq.utils.s3.s3_utils import S3Utils
from dataacq.dataacq.sec_master.const import BUCKET_NAME,\
    SQL_CREDENTIALS, EODHD_SEARCH_API,\
    EODHD_API_KEY


class Fundamental:

    """
    TODO: We have to split what we receive into multiple insert queries.

    This should be two multiple write functions here.
    """

    def __init__(self):
        """Instantiate Fundamental Scraper."""
        self.s3_client = S3Utils(
            BUCKET_NAME
        )
        self.sql_client = SQLUtils(
            **SQL_CREDENTIALS
        )

    def 