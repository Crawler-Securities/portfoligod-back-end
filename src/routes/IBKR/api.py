from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from src.config import CPAPI_GATEWAY_URL

from src.routes.IBKR.ProxyCPAPI import ProxyCPAPI
from src.routes.utils import parsers

router = APIRouter()
cpapi_prox = ProxyCPAPI(CPAPI_GATEWAY_URL)


@router.get("/connection-status")
def check_cpapi_connection():
    gateway_response = cpapi_prox.check_cpapi_auth_status()
    content: dict = {}
    if gateway_response.status_code == 200:
        content['connected'] = True
    elif gateway_response.status_code == 401:
        content['connected'] = False
    else:
        raise Exception(f"Unexpected status code: {gateway_response.status_code}")
    return JSONResponse(content=content, media_type="application/json")


@router.get("/login-page")
def get_login_page():
    return RedirectResponse(url=CPAPI_GATEWAY_URL, status_code=307)
