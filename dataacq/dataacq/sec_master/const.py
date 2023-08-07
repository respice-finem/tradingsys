from datetime import date
import os

EODHD_SEARCH_API = 'https://eodhistoricaldata.com/api/search/'
EODHD_API_KEY = os.getenv('EODHD_API_KEY')
BUCKET_NAME = 'tradingsys'
SEC_MASTER_URL = 'https://files.catnmsplan.com/symbol-master/FINRACATReportableEquitySecurities_EOD.txt'
TODAY = date.today().strftime('%Y-%m-%d')
SEC_MASTER_FILE_NAME = f'dataacq/sec_master/security_master_{TODAY}.txt'
SEC_MASTER_ENRICHED_FILE_NAME = f'dataacq/sec_master/security_master_enriched_{TODAY}.json'
SEC_MASTER_EXCH_MAP ={
    'A': 'NYSE American',
    'N': 'NYSE',
    'O': 'OTCBB',
    'P': 'NYSE ARCA',
    'Q': 'Nasdaq',
    'U': 'OTC Equity',
    'V': 'IEX',
    'Z': 'Cboe BZX'
}
S3_ENV_VARS = [
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY'
]
SQL_CREDENTIALS = {
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}