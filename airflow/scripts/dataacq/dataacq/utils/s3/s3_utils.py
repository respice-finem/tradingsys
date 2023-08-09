import boto3
import os
import io

from dataacq.dataacq.sec_master.const import S3_ENV_VARS
from dataacq.dataacq.utils.error import EnvironmentVariableMissingError

class S3Utils:

    def __init__(
        self,
        bucket_name,

    ):
        """Instantiate S3 Utils."""
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    def validate(
        self
    ):
        """
        Validate whether environment variables are available for S3
        """
        for ENV_VAR in S3_ENV_VARS:
            if not os.getenv(ENV_VAR):
                raise EnvironmentVariableMissingError(f'{ENV_VAR} is missing, please include it in environment')

    def read(
        self,
        prefix: str
    ):
        """
        Read items from object.
        """
        response = self.s3_client.get_object(
            Bucket=self.bucket_name,
            Key=prefix
        )
        return response
    
    def write(
        self,
        file_content: bytes,
        file_name: str
    ):
        """
        TODO:
        REFACTOR LATER TO HANDLE DIFFERENT FILE TYPES

        Arguments:
            file_content: Content of file in bytes
            file_name: Prefix of file name to be included in our S3 bucket
       
        Returns:
        """
        self.validate()
        with io.BytesIO(file_content) as output_file:
            response = self.s3_client.upload_fileobj(
                output_file,
                self.bucket_name,
                file_name
            )
        return response