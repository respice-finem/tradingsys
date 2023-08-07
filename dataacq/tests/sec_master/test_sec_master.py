from dataacq.dataacq.sec_master.sec_master import SecurityMaster
from unittest.mock import patch

enrich_output = ("US00846U1016", "Agilent Technologies Inc", "Common Stock")
file_content = b'symbol|issueName|listingExchange|testIssueFlag\nA|Agilent Technologies Inc.|N|N'

@patch("dataacq.dataacq.sec_master.sec_master.SecurityMaster.enrich")
def test_security_master_full_enrich(
    mock_enrich
):
    """Test if security master enrichment works."""
    sm = SecurityMaster()
    mock_enrich.return_value = enrich_output
    actual_output = sm.full_enrich(file_content)
    assert actual_output == {
        0: {
            "symbol": "A",
            "issueName": "Agilent Technologies Inc",
            "listingExchange": "NYSE",
            "ISIN": "US00846U1016",
            "securityType": "Common Stock",
            "country": "US"
        }
    }

@patch("dataacq.dataacq.sec_master.sec_master.SQLUtils.query")
@patch("dataacq.dataacq.sec_master.sec_master.SecurityMaster.enrich")
@patch("dataacq.dataacq.sec_master.sec_master.SecurityMaster.get_file_content")
def test_security_master_process(
    mock_file_content,
    mock_single_enrich,
    mock_query
):
    """Test if security master process works"""
    sm = SecurityMaster()
    mock_file_content.return_value = file_content
    mock_single_enrich.return_value = enrich_output
    mock_query.return_value = None
    actual_output = sm.process()
    assert actual_output == [(
        "US00846U1016",
        "A",
        "NYSE",
        "Agilent Technologies Inc",
        "US",
        "Common Stock"
    )]