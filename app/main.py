from fastapi import FastAPI
from datetime import datetime, timedelta
from app.auth import router as auth_router
from app.token import router as token_router
from app.events import router as events_router

app = FastAPI()

# ⬇⬇⬇ Bu endpoint'i include_router'lardan ÖNCE ekle
@app.get("/available-hours")
def get_available_hours():
    start_hour = 8
    end_hour = 17
    excluded_hour = 12
    interval = 60

    hours = []
    current_time = datetime.strptime(f"{start_hour}:00", "%H:%M")
    end_time = datetime.strptime(f"{end_hour}:00", "%H:%M")

    while current_time < end_time:
        if current_time.hour != excluded_hour:
            hours.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=interval)

    return {"available_hours": hours}

# Router'lar en son
app.include_router(events_router)
app.include_router(auth_router)
app.include_router(token_router)

@app.get("/")
def root():
    return {"message": "Zoho Randevu API Sistemi Aktif"}
