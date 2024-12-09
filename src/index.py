"""
Application entrypoint
"""

# Import external modules
import asyncio
import os
import sys
from hypercorn.asyncio import serve as hypercorn_serve
from hypercorn.config import Config as HypercornConfig
from quart import Quart

# Import modules in subfolders relative to folder where Python process started, i.e. src/index.py
from api.api_response import ApiResponse
from api.routes import routes as api_routes

def main():
    """
    Main function

    :rtype: None
    """

    # Add exception handler
    def uncaught_exception_handler(exception_type, exception_value, exception_traceback):
        """
        Handle uncaught exceptions in main thread
        See https://stackoverflow.com/a/16993115

        :param: str exception_type Type of exception
        :param: str exception_value Exception message
        :param: str exception_traceback Exception traceback
        :rtype: None
        """
        print('Uncaught exception in main thread')
        print(exception_type)
        print(exception_value)
        print(exception_traceback)
    # end def uncaught_exception_handler
    sys.excepthook = uncaught_exception_handler

    # Instantiate server
    app = Quart(__name__)

    # Add error handler
    @app.errorhandler(Exception)
    def app_error_handler(err):
        """
        Handle uncaught exceptions in app routes
        See https://flask.palletsprojects.com/en/stable/errorhandling/

        :param: Exception err
        :rtype: dict
        """
        print('Uncaught exception in app')
        print(err)
        response = ApiResponse(500, str(err))

        return response.to_dict(), response.meta['status_code']
    # end def app_error_handler

    # Add routes
    api_routes(app)

    # Server config - see https://hypercorn.readthedocs.io/en/latest/how_to_guides/configuring.html
    internal_port = os.getenv('DEMO_PORT_INTERNAL', '9000')
    server_config = HypercornConfig()
    server_config.bind = [f"0.0.0.0:{internal_port}"] # listen on all IPs else not accessible outside Docker container
    server_config.loglevel = 'CRITICAL' # reduce log noise from Hypercorn

    # Start server programmatically instead of starting it via commandline
    # See https://hypercorn.readthedocs.io/en/latest/how_to_guides/api_usage.html
    print(f"Server started listening at port {internal_port}.") # this must come before serve() for it to show
    asyncio.run(hypercorn_serve(app, server_config))
# end def main

# Run application
if __name__ == '__main__':
    main()
# end if
