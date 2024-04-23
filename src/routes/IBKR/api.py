from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Request

from starlette.responses import RedirectResponse, Response
import httpx

from src.config import CPAPI_GATEWAY_URL

from src.routes.IBKR.ProxyCPAPI import ProxyCPAPI

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


@router.api_route('/proxy/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def proxy_route(request: Request, path: str):
    # The URL to which you want to proxy the requests
    target_url = f'{CPAPI_GATEWAY_URL}/{path}'


    # Include headers from the original request in the proxy request
    # You might want to exclude some headers, like Host
    headers = {key: value for key, value in request.headers.items() if key.lower() != 'host'}

    # Asynchronously send the request to the target URL with the original body, method, and headers
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.query_params,
            data=await request.body(),
            follow_redirects=True,

        )

    # Return the response received from the target
    return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))
