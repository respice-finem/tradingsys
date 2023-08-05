import psycopg2

from dataacq.utils.error import NoDataWriteError

class SQLUtils:

    """
    This class does the following:

    1)
    """

    def __init__(
        self,
        **kwargs
    ):
        """
        Instantiate SQL class
        """
        self.database = kwargs['database']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.host = kwargs['host']
        self.port = kwargs['port']
    
    def query(
        self,
        query: str,
        data: list = [],
        qtype: str = 'read',
    ):
        """
        Perform specific query.

        Arugments:
            query: SQL query in string format
            read: Whether is a read query
        Returns:
            response: Returns tuples of SQL output if read is true,
            else None
        """
        if qtype == 'write' and not data:
            raise NoDataWriteError("Can't do write without data provided")

        response = None
        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cursor = conn.cursor()
        cursor.execute(query)
        
        if qtype == 'read':
            response = cursor.fetchall()
        conn.commit()
        conn.close()
        return response
