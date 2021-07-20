import redis
import fastapi, json
from pydantic import BaseModel
from typing import List

db = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = fastapi.FastAPI()

class NewsFlow(BaseModel):
    news: List[int]

class Data(BaseModel):
    value: str

@app.get('/')
async def status_report():
    return {
        "status": "Redis all green" 
    }

@app.get('/{key}')
def get_value(key):
    response = db.get(key).replace("NaN", "0")
    return json.loads(response)
@app.post('/{key}')
def set_value(key: str, data: Data):
    db.set(key, data.value)
    raise fastapi.HTTPException(200)

@app.get('/top/{datetime}/{quote}')
def get_news_flow(datetime: str, quote: str):
    return json.loads(db.get(datetime + "-" + quote))

@app.post('/top/{datetime}/{quote}')
def set_news_flow(datetime: str, quote: str, value: NewsFlow):
    db.set(datetime + "-" + quote, json.dumps(value.dict()))
    raise fastapi.HTTPException(200)
