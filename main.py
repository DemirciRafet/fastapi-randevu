from fastapi import FastAPI
from app.auth import router as auth_router
from app.token import router as token_router
from app.events import router as events_router
app = FastAPI()  # Önce uygulamayı tanımlıyoruz

# Router'ları sırayla ekliyoruz
app.include_router(events_router)
app.include_router(auth_router)
app.include_router(token_router)


@app.get("/")
def root():
    return {"message": "Zoho Randevu API Sistemi Aktif"}
