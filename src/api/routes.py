# Import external modules
from quart import websocket

# Import internal modules
from api.api_response import ApiResponse
from app.helper import helper

def routes(app):
    """
    Routes for API component

    :param: quart.app.Quart app
    :rtype: None
    """

    """
    All endpoints will return ApiResponse.

    Note that "apiSuccess {object} data" must be redeclared in the API
    docblock for individual endpoints else properties under data,
    e.g. "apiSuccess {object} data.username", will come under error/meta key
    in generated HTML. Same for error and meta if additional properties are
    to be added under them.

    @apiDefine ApiResponse
    @apiHeader {string} Content-Type application/json
    @apiSuccess {object} data All properties for success response put in here.
    @apiSuccess {null} error This will be set to null for success response.
    @apiSuccess {object} meta Metadata such as status code and pagination.
    @apiSuccess {number} meta.status_code HTTP status code for success response.
    @apiSuccess {string} meta.request_id Unique ID computed for each request to group all
        audit records created for a request, e.g. for database access.
    @apiSuccess {string} meta.version Application version.
    @apiError (Error) {null} data This will be set to null for error response.
    @apiError (Error) {object} error All properties for error response put in here.
    @apiError (Error) {string} error.message Error message.
    @apiError (Error) {object} meta Metadata such as status code and pagination.
    @apiError (Error) {number} meta.status_code HTTP status code for error response.
    @apiError (Error) {string} meta.request_id Unique ID computed for each request to group all
        audit records created for a request, e.g. for database access.
    @apiError (Error) {string} meta.version Application version.
    @apiErrorExample {application/json} Error (not allowed action on record):
        HTTP/1.1 403 Forbidden
        {
          "data": null,
          "error": {
            "message": "Forbidden from <action name> action on <resource name> resource."
          },
          "meta": {
            "status_code": 400,
            "request_id": "1631175138159-ac98f1c3-df0e-40b1-81f9-3c03bcdf6135",
            "version": "v0.10.0-develop-f94fda8-20211122T0156Z"
          }
        }
    """

    @app.websocket('/ws')
    async def ws():
        """
        Websocket handler for /ws

        To test, create a test.html with the following contents and open it in
        a browser:
            <script>
                // This will not run if pasted in console directly due to Content Security Policy
                let socket = new WebSocket('ws://localhost:10000/ws');
                socket.addEventListener('message', (event) => {
                    console.log(event.data);
                });
                socket.addEventListener('open', (event) => {
                    console.log('Websocket connection established.');
                    socket.send('Hello World');
                });
            </script>
        """
        while True:
            data = await websocket.receive()
            print(data, flush=True)
            await websocket.send(data)
        # end while
    # end def ws

    @app.route('/healthcheck', methods=['GET'])
    async def healthcheck():
        """
        Route handler for /healthcheck

        :return: JSON response
        :rtype: tuple(dict, int)

        @api {get} /healthcheck Health Check
        @apiName HealthCheck
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
            'timestamp': helper.timestamp(seconds_only=True),
        })

        return response.to_dict(), response.meta['status_code']
    # end def healthcheck

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    async def catchall(path):
        """
        Route handler for catch-all route

        :return: JSON response
        :rtype: tuple(dict, int)

        @api {get} / Catch-All
        @apiName CatchAll
        @apiGroup System
        @apiDescription All unmatched routes, e.g. /api/invalid-route, are
            handled by this. Note that there is no success response.

        @apiExample {curl} Example usage:
            curl --location --request GET "http://localhost:10000/invalid-route"
            --header "Content-Type: application/json"

        @apiUse ApiResponse
        @apiErrorExample {application/json} Error (not found):
            HTTP/1.1 404 Not Found
            {
              "data": null,
              "error": {
                "message": "Endpoint /invalid-route not found."
              },
              "meta": {
                "status_code": 404,
                "request_id": "1631679055974-89d413c2-6e44-440d-ab3c-9767a91a3f50",
                "version": "v0.10.0-develop-f94fda8-20211122T0156Z"
              }
            }
        """
        response = ApiResponse(404, f"Endpoint /{path} not found.")

        return response.to_dict(), response.meta['status_code']
    # end def catchall
# end def routes
