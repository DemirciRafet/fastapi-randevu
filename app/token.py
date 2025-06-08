from fastapi import APIRouter, HTTPException, Query
from app.config import ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REDIRECT_URI
import httpx, json

router = APIRouter()

@router.get("/callback")
async def get_token(code: str = Query(...)):
    # Zoho API URL
    url = "https://accounts.zoho.eu/oauth/v2/token"
    
    # Token almak için gönderilecek data
    data = {
        "grant_type": "authorization_code",
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "redirect_uri": ZOHO_REDIRECT_URI,
        "code": code
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Token yenileme isteği
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
    
    # Hata kontrolü
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Token alma işlemi başarısız.")

    # Zoho'dan dönen JSON veri
    token_data = response.json()

    # Yeni token'ı token.json dosyasına kaydet
    with open("app/token.json", "w") as f:
        json.dump({"access_token": token_data["access_token"]}, f)

    return {"message": "Yeni access token alındı", "access_token": token_data["access_token"]}
