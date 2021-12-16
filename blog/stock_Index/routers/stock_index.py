import ssl
from fastapi import APIRouter
from fastapi.params import Path

from blog.stock_Index import table_parser
from blog.stock_Index.models import CompanyName, Index, MyException
from blog.util import json_error

router = APIRouter(
    tags=["stock-index"],
    prefix="/stock-index"
)


ssl._create_default_https_context = ssl._create_unverified_context


@router.get('/{index}')
async def get(index: Index = Path(..., title="The name of the Index")):
    if index == Index.SNP500:
        companies = await table_parser.get_sp500_companies()
    elif index == Index.FTSE100:
        companies = await table_parser.get_ftse_companies()
    else:
        return json_error(418, f"Error occurred! Please contact the system admin...")

    return companies
