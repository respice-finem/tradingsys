"""This module contains the API scraper."""
import requests
from scripts.dataacq.dataacq.utils.s3.s3_utils import S3Utils
import logging
from scripts.dataacq.dataacq.utils.error import BucketNameUnavailableError

class APIScraper:

    def __init__(
        self,
        url: str,
        bucket_name: str = None
    ):
        """
        Instantiate our API scraper class.
        """
        self.initial_url = url
        self.bucket_name = bucket_name
        if self.bucket_name:
            self.s3_client = S3Utils(
                self.bucket_name
            )

    def request(
        self
    ) -> bytes:
        """
        Performs API call to read from URL.
        
        Returns:
            response_content: Bytes content from response
        """
        try:
            # TODO: Future refactoring needed for complex calls i.e. validation related stuff
            response = requests.get(self.initial_url)
            return response.content
        except requests.exceptions.RequestException as err:
            logging.error(f'Requests invalid: {err}')
        except requests.exceptions.HTTPError as errh:
            logging.error(f'Requests valid, HTTP Error met: {errh}')
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Connection issues: {errc}")
        except requests.exceptions.Timeout as errt:
            logging.error(f'Timeout issue: {errt}')

    def scrape(
        self,
        file_name: str
    ):
        """
        Main function for our scraper.

        TODO: Refactor to handle bad responses
        """
        if not self.bucket_name:
            raise BucketNameUnavailableError('Provide a bucket to store the scraped output.')
        file_content = self.request()
        response = self.s3_client.write(
            file_content,
            file_name
        )
        return response