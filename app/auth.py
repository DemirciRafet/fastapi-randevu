from fastapi import APIRouter
from app.config import ZOHO_CLIENT_ID, ZOHO_REDIRECT_URI

router = APIRouter()

SCOPE = "ZohoCalendar.calendar.ALL"

@router.get("/login")
def get_auth_url():
    url = (
        "https://accounts.zoho.eu/oauth/v2/auth?"
        f"scope={SCOPE}&client_id={ZOHO_CLIENT_ID}&"
        f"response_type=code&access_type=offline&redirect_uri={ZOHO_REDIRECT_URI}"
    )
    return {"auth_url": url}
