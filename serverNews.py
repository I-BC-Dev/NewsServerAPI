import requests
from fastapi import FastAPI
from fastapi.responses import Response
import uvicorn
import time

app = FastAPI()

URL = "http://nfs.faireconomy.media/ff_calendar_thisweek.xml"
headers = {"User-Agent": "Mozilla/5.0 (compatible; CacheServer/1.0)"}

cache = {"timestamp": 0.0, "data": ""}
CACHE_DURATION = 400  # 5 minutes in seconds


def fetch_calendar_xml():
    current_time = time.time()
    if current_time - cache["timestamp"] < CACHE_DURATION:
        return cache["data"]

    response = requests.get(URL, headers=headers)
    print("Server News Request: ", response.status_code)
    response.raise_for_status()
    cache["data"] = response.text
    cache["timestamp"] = current_time
    return cache["data"]


@app.get("/api/calendar")
def get_calendar():
    try:
        xml_data = fetch_calendar_xml()
        return Response(content=xml_data, media_type="application/xml")
    except Exception as e:
        return Response(content=f"<error>{str(e)}</error>", media_type="application/xml", status_code=500)


@app.get("/")
def root():
    return {"message": "News Server API"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=1225)
