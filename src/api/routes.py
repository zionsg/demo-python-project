from api.api_response import ApiResponse
from app.helper import helper

def routes(app):
    """
    Routes for API component

    :param: quart.app.Quart app
    :rtype: None
    """

    @app.route('/healthcheck', methods=['GET'])
    async def healthcheck():
        """
        Route handler for /healthcheck

        :return: JSON response
        :rtype: dict

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
        response = ApiResponse(200, '', {
            'message': 'OK',
            'timestamp': helper['timestamp'](seconds_only=True),
        })

        return response.to_dict(), response.meta['status_code']
    # end def healthcheck
# end def routes
