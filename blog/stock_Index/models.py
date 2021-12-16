from enum import Enum, IntEnum

from pydantic.main import BaseModel


class Index(str, Enum):
    FTSE100 = "FTSE 100"
    SNP500 = "S&P 500"
    DOWJONE = "Dow Jones"


class IntIndex(Enum):
    FTSE100 = 1
    SNP500 = 2
    DOWJONE = 3


class MyException(Exception):
    pass


class CompanyName(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Company():
    def __init__(self, symbol):
        self.name = None
        self.symbol = symbol
        self.sector = None
        self.industry = None


index_map = {Index.FTSE100: 'https://en.wikipedia.org/wiki/FTSE_100_Index',
             Index.SNP500: 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'}
