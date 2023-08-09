"""This module contains parse function for our workflow."""

from dataacq.dataacq.sec_master.sec_master import SecurityMaster

def process():
    sm = SecurityMaster()
    _ = sm.process()
