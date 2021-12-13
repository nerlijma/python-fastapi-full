
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def get():
    return {"msg": 'site is up'}
