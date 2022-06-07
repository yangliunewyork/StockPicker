"""
NasdaqDataCollector is  class to pull tickers list from Nasdap.
Nasdap upload tickers information to a text file in their FTP server every day.
This class login the FTP server and parse the text file to get all the tickers.
"""
from ftplib import FTP
from io import StringIO


class NasdaqDataCollector:
    """
    A class to pull tickers list from Nasdap.
    Nasdap upload tickers information to a text file in their FTP server every day.
    This class login the FTP server and parse the text file to get all the tickers.
    """

    def get_tickers(self):
        """
        Send http request to get stock information.
        Return a stocks HashMap, <"symbol", Stock>
        """
        ftp = FTP("ftp.nasdaqtrader.com")
        ftp.login()
        ftp.cwd("/SymbolDirectory/")

        data = StringIO()
        ftp.retrbinary(
            "RETR nasdaqlisted.txt", lambda block: data.write(block.decode("utf-8"))
        )
        ftp.quit()
        data.seek(0)  # Change the stream position to the byte offset `0`
        tickers = []
        for line in data:
            array = line.split("|")
            # print (array[0])
            tickers.append(array[0])
        return tickers


if __name__ == "__main__":
    nasdaqDataCollector = NasdaqDataCollector()
    nasdaq_tickers = nasdaqDataCollector.get_tickers()
    print(nasdaq_tickers)
