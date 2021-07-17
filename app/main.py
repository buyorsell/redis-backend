import redis
import fastapi, json
from pydantic import BaseModel
from typing import List
import base64

db = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = fastapi.FastAPI()

class NewsFlow(BaseModel):
	news: List[int]

@app.get('/')
def status_report():
	return {
		"status": "Redis all green" 
	}

@app.get('/{key}')
def get_value(key):
	response = db.get(key)
	try:
		return json.loads(response)
	except:
		return response

@app.post('/{key}/{value}')
def set_value(key, value):
    try:
        db.set(key, base64.urlsafe_b64decode(value))
    except:
        db.set(key, value)
    raise fastapi.HTTPException(200)

@app.get('/top/{datetime}/{quote}')
def get_news_flow(datetime: str, quote: str):
    return json.loads(db.get(datetime + "-" + quote))

@app.post('/top/{datetime}/{quote}')
def set_news_flow(datetime: str, quote: str, value: NewsFlow):
    db.set(datetime + "-" + quote, json.dumps(value.dict()))
    raise fastapi.HTTPException(200)
