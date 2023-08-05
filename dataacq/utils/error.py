class EnvironmentVariableMissingError(Exception):
    """Indicate environment variables are missing."""
    pass

class BucketNameUnavailableError(Exception):
    """Indicate bucket name is missing."""
    pass

class NoDataWriteError(Exception):
    """Indicate non read query is inpermissible."""
    pass