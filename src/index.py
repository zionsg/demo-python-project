"""
  Application entrypoint
"""

import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from quart import Quart, render_template

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
        "message": "OK"
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
    return {
        "data": {
            "message": "Hello World!"
        },
        "error": None,
        "meta": {
            "version": "0.1.0",
        },
    }
# end def healthcheck

# Server config - see https://hypercorn.readthedocs.io/en/latest/how_to_guides/configuring.html
config = Config()
config.bind = ["localhost:8080"]

# Start server programmatically instead of starting it via commandline using `hypercorn module:index`
# See https://hypercorn.readthedocs.io/en/latest/how_to_guides/api_usage.html#graceful-shutdown
asyncio.run(serve(app, config))
