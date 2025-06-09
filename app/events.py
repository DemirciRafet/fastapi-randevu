from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import httpx

router = APIRouter()

class EventRequest(BaseModel):
    date: str  # Örnek: 2025-06-11
    time: str  # Örnek: 14:00
    title: str  # Örnek: Görüşme, Randevu, Danışmanlık

ZOHO_ACCESS_TOKEN = 'your_access_token_here'  # Buraya Zoho Access Token'ı ekleyin

@router.post("/create-event")
async def create_event(data: EventRequest):
    try:
        # Sabit bir zaman formatı kullanalım: "14:00"
        time_parts = data.time.split(":")
        
        if len(time_parts) != 2:
            raise HTTPException(status_code=400, detail="Zaman formatı hatalı, lütfen saat:dakika formatında girin.")

        # Saat ve dakikayı alalım
        start_hour = int(time_parts[0])  # Saat
        start_minute = int(time_parts[1])  # Dakika

        # Bitiş saatini hesaplayalım
        end_hour = start_hour + 1
        end_time = f"{end_hour:02d}:{start_minute:02d}"

        # Randevu zamanlarını oluştur
        start_datetime = f"{data.date}T{data.time}:00"
        end_datetime = f"{data.date}T{end_time}:00"

        # Event verisini hazırlayalım
        event_data = {
            "data": [{
                "Event_Title": data.title,
                "Start_DateTime": start_datetime,
                "End_DateTime": end_datetime
            }]
        }

        # Zoho API'ye veri gönder
        headers = {
            "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.zohoapis.eu/crm/v6/Events",
                json=event_data,
                headers=headers
            )

        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return {"message": "Event oluşturuldu", "zoho_response": response.json()}

    except ValueError:
        raise HTTPException(status_code=400, detail="Zaman formatı hatalı, lütfen saat:dakika formatında girin.")
