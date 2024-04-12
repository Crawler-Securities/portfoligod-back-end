from fastapi.routing import APIRouter

from src.config import CPAPI_GATEWAY_URL

from src.routes.IBKR.ProxyCPAPI import ProxyCPAPI

router = APIRouter()
cpapi_prox = ProxyCPAPI(CPAPI_GATEWAY_URL)


@router.get("/connection-status")
def check_cpapi_connection():
    gateway_response = cpapi_prox.check_cpapi_auth_status()
    return gateway_response
