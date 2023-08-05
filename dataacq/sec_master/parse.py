"""This module contains parse function for our workflow."""

from dataacq.sec_master.sec_master import SecurityMaster

def process():
    sm = SecurityMaster()
    sm.process()

if __name__ == '__main__':
    process()