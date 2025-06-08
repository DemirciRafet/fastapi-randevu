import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # Pydantic modelini ekliyoruz
import httpx

router = APIRouter()

# EventRequest Modeli
class EventRequest(BaseModel):
    date: str  # örnek: 2025-06-11
    time: str  # örnek: 14:00
    title: str  # örnek: Görüşme, Randevu, Danışmanlık

# token.json'dan access_token'ı oku
def get_access_token():
    with open("app/token.json", "r") as f:
        token_data = json.load(f)
    return token_data["access_token"]

@router.post("/create-event")
async def create_event(data: EventRequest):
    access_token = get_access_token()  # Token'ı oku

    # Event başlatma verilerini hazırla
    start_datetime = f"{data.date}T{data.time}:00"
    end_hour = int(data.time.split(":")[0]) + 1
    end_datetime = f"{data.date}T{end_hour:02d}:{data.time.split(':')[1]}:00"

    payload = {
        "data": [{
            "Event_Title": data.title,
            "Start_DateTime": start_datetime,
            "End_DateTime": end_datetime
        }]
    }

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    # Zoho API'ye istek gönder
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.zohoapis.eu/crm/v6/Events",
            json=payload,
            headers=headers
        )

    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"message": "Event oluşturuldu", "zoho_response": response.json()}
