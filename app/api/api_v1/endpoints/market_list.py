import secrets

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import JSONResponse

from app.coinex.market_list import MarketList

router = APIRouter()
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "lpm")
    correct_password = secrets.compare_digest(credentials.password, "123")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/market_list")
async def get_market_list():
    # username: str = Depends(get_current_username)):
    data = MarketList().fetch()
    return JSONResponse(status_code=status.HTTP_200_OK, content=
    {
        "market_list": data['data']
    })


