import logging

from dataacq.dataacq.utils.scraper.apiScraper import APIScraper
from dataacq.dataacq.sec_master.const import SEC_MASTER_URL,\
    SEC_MASTER_FILE_NAME, BUCKET_NAME


def scrape():
    ascraper = APIScraper(
        SEC_MASTER_URL,
        BUCKET_NAME
    )
    file_name = SEC_MASTER_FILE_NAME
    response_content = ascraper.scrape(
        file_name
    )
    logging.info(response_content)

if __name__ == '__main__':
    scrape()