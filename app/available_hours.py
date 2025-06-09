from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import httpx

router = APIRouter()

@router.get("/available-hours")
async def get_available_hours(date: str):
    # Zoho Calendar API'sinden müsait saatleri almak için buraya API çağrısı ekle
    start_hour = 8
    end_hour = 17
    excluded_hour = 12
    interval = 60  # 60 dakika

    hours = []
    current_time = datetime.strptime(f"{start_hour}:00", "%H:%M")
    end_time = datetime.strptime(f"{end_hour}:00", "%H:%M")

    while current_time < end_time:
        if current_time.hour != excluded_hour:
            hours.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=interval)

    return {"available_hours": hours}
