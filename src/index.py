"""
Application entrypoint
"""

# Import external modules
import asyncio
from hypercorn.asyncio import serve as hypercorn_serve
from hypercorn.config import Config as HypercornConfig
from quart import Quart

# Import modules in subfolders relative to folder where Python process started, i.e. src/index.py
from api.api_response import ApiResponse
from app.helper import helper

# Instantiate server
app = Quart(__name__)

"""
@api {get} /healthcheck Health Check
@apiName Health Check
@apiGroup System
@apiDescription Authentication not required. This endpoint is used for
    healthcheck in `docker-compose.yml`.
    <p>Note that there is no `/api` prefix so that other middleware need
    not be loaded. In production, this endpoint should be blocked by Nginx or
    the load balancer so that it can only be called within the host machine,
    private network or office VPN, and not from the public Internet.</p>

@apiExample {curl} Example usage:
    curl --location --request GET "http://localhost:10000/healthcheck"
    --header "Content-Type: application/json"

@apiUse ApiResponse
@apiSuccess {object} data All properties for success response put in here.
@apiSuccess {string} data.message Short message.
@apiSuccessExample {application/json} Success:
    HTTP/1.1 200 OK
    {
      "data": {
        "message": "OK",
        "timestamp": "2024-11-28T00:10:30Z"
      },
      "error": null,
      "meta": {
        "status_code": 200,
        "request_id": "1631679055974-89d413c2-6e44-440d-ab3c-9767a91a3f50",
        "version": "v0.10.0-develop-f94fda8-20211122T0156Z"
      }
    }
"""
@app.route('/healthcheck')
async def healthcheck():
    """
    Route handler for /healthcheck

    :return: JSON response
    :rtype: dict
    """

    response = ApiResponse(200, '', {
        'message': 'OK',
        'timestamp': helper['timestamp'](seconds_only=True),
    })

    return response.to_dict()
# end def healthcheck

# Server config - see https://hypercorn.readthedocs.io/en/latest/how_to_guides/configuring.html
server_config = HypercornConfig()
server_config.bind = ['localhost:10000']

# Start server programmatically instead of starting it via commandline
# See https://hypercorn.readthedocs.io/en/latest/how_to_guides/api_usage.html
asyncio.run(hypercorn_serve(app, server_config))
