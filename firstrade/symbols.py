from bs4 import BeautifulSoup

from firstrade import urls
from firstrade.account import FTSession


class SymbolQuote:
    """
    Dataclass containing quote information for a symbol.

    Attributes:
        ft_session (FTSession):
            The session object used for making HTTP requests to Firstrade.
        symbol (str): The symbol for which the quote information is retrieved.
        exchange (str): The exchange where the symbol is traded.
        bid (float): The bid price for the symbol.
        ask (float): The ask price for the symbol.
        last (float): The last traded price for the symbol.
        change (float): The change in price for the symbol.
        high (float): The highest price for the symbol during the trading day.
        low (float): The lowest price for the symbol during the trading day.
        volume (str): The volume of shares traded for the symbol.
        company_name (str): The name of the company associated with the symbol.
        real_time (bool): If the quote is real-time or not
        fractional (bool):  If the stock can be traded fractionally, or not
    """

    def __init__(self, ft_session: FTSession, symbol: str):
        """
        Initializes a new instance of the SymbolQuote class.

        Args:
            ft_session (FTSession):
                The session object used for making HTTP requests to Firstrade.
            symbol (str): The symbol for which the quote information is retrieved.
        """
        self.ft_session = ft_session
        self.symbol = symbol
        symbol_data = self.ft_session.get(
            url=urls.quote(self.symbol), headers=urls.session_headers()
        )
        soup = BeautifulSoup(symbol_data.text, "xml")
        quote = soup.find("quote")
        self.symbol = quote.find("symbol").text
        self.exchange = quote.find("exchange").text
        self.bid = float(quote.find("bid").text.replace(",", ""))
        self.ask = float(quote.find("ask").text.replace(",", ""))
        self.last = float(quote.find("last").text.replace(",", ""))
        self.change = float(quote.find("change").text.replace(",", ""))
        if quote.find("high").text == "N/A":
            self.high = None
        else:
            self.high = float(quote.find("high").text.replace(",", ""))
        if quote.find("low").text == "N/A":
            self.low = "None"
        else:
            self.low = float(quote.find("low").text.replace(",", ""))
        self.volume = quote.find("vol").text
        self.company_name = quote.find("companyname").text
        self.real_time = quote.find("realtime").text == "T"
        self.fractional = quote.find("fractional").text == "T"
