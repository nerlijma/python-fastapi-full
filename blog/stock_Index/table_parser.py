from typing import List
import pandas as pd

from blog.stock_Index.models import Company


async def get_sp500_companies() -> List:
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table: List = pd.read_html(url)[0]
    # print(table)
    companies = []

    for index, row in table.iterrows():
        company = Company(row['Symbol'])
        company.name = row['Security']
        company.sector = row['GICS Sector']
        company.industry = row['GICS Sub-Industry']
        company.date_added = row['Date first added']
        companies.append(company)

    array_of_names = [c.name for c in companies]
    return array_of_names


async def get_ftse_companies() -> List:
    url = 'https://en.wikipedia.org/wiki/FTSE_100_Index'
    table: List = pd.read_html(url)[3]
    print(table)
    companies = []

    for index, row in table.iterrows():
        company = Company(row['EPIC'])
        company.name = row['Company']
        company.sector = ['FTSE Industry Classification Benchmark sector[13]']
        companies.append(company)

    array_of_names = [c.name for c in companies]
    return array_of_names
