from scripts.dataacq.dataacq.sec_master.ohlc import OHLC
from unittest.mock import patch
from datetime import datetime


@patch("scripts.dataacq.dataacq.sec_master.ohlc.SQLUtils.query")
def test_ohlc_get_tickers(mock_query):
    """Test whether OHLC process works."""
    mock_query.return_value = [
        (
            "US5949181045",
            "MSFT",
            "Nasdaq",
            "Microsoft Corporation",
            "US",
            "Common Stock"
        )
    ]
    ohlc = OHLC()
    ticker_dict = ohlc.get_tickers()
    assert ticker_dict == {
        "US5949181045": "MSFT.US"
    }

@patch("scripts.dataacq.dataacq.sec_master.ohlc.SQLUtils.query")
@patch("scripts.dataacq.dataacq.sec_master.ohlc.OHLC.get_data")
@patch("scripts.dataacq.dataacq.sec_master.ohlc.OHLC.get_tickers")
def test_ohlc_process(
    mock_ticker,
    mock_data,
    mock_query
    ):
    """Test whether OHLC process works."""
    mock_ticker.return_value = {
        "US5949181045": "MSFT.US"
    }
    mock_data.return_value = [(
        "US5949181045",
        326.02,
        328.26,
        321.18,
        322.93,
        322.93,
        20113700,
        "2023-08-11"
    )]
        
    mock_query.return_value = None

    ohlc = OHLC()
    full_ohlcv_data = ohlc.process(
        "2023-08-11",
        "2023-08-11"
    )
    assert full_ohlcv_data == [
        (
        "US5949181045",
        326.02,
        328.26,
        321.18,
        322.93,
        322.93,
        20113700,
        "2023-08-11"
        )
    ]