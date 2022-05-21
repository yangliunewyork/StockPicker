#!/usr/bin/python
import requests
import csv

from ftplib import FTP
#from io import BytesIO
from io import StringIO

from Model.Stock import Stock


class NasdaqTracker:
    """
    A class to pull tickers list from Nasdap.
    Here is what you cant get:
    ["Symbol","Name","LastSale","MarketCap","IPOyear",
    "Sector","industry","Summary Quote"]
    """

    def __init__(self):
        self.nasdaq_url = "ftp.nasdaqtrader.com/SymbolDirectory ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"

    def get_tickers(self):
        """
        Send http request to get stock information.
        Return a stocks HashMap, <"symbol", Stock>
        """
        ftp = FTP('ftp.nasdaqtrader.com')
        ftp.login()
        ftp.cwd("/SymbolDirectory/")
        myfiles = ftp.dir()
        #print (myfiles)

        data = StringIO()
        ftp.retrbinary('RETR nasdaqlisted.txt',
                       lambda block: data.write(block.decode('utf-8')))
        ftp.quit()
        data.seek(0)  # Change the stream position to the byte offset `0`
        tickers = []
        for line in data:
            array = line.split("|")
            # print (array[0])
            tickers.append(array[0])
        return tickers


if __name__ == "__main__":
    tracker = NasdaqTracker()
    tickers = tracker.get_tickers()
    print(tickers)
