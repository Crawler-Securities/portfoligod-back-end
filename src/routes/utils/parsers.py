import requests
import fastapi


def convert_to_fastapi_response(response: requests.Response):
    return fastapi.Response(content=response.content,
                            status_code=response.status_code,
                            headers=dict(response.headers),
                            media_type=response.headers['Content-Type'])

