"""
Application entrypoint
"""

# Import external modules
import asyncio
import sys
from hypercorn.asyncio import serve as hypercorn_serve
from hypercorn.config import Config as HypercornConfig
from quart import Quart, request # request needed in order to access the request inside route handlers

# Import internal modules in subfolders relative to folder where Python process started, i.e. src/index.py
from api.api_response import ApiResponse
from api.routes import routes as api_routes
from app.config import config
from app.logger import logger

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
        :param: Exception exception_value Exception object
        :param: str exception_traceback Exception traceback
        :rtype: None
        """
        logger.error(None, 'Uncaught exception in main thread.', exception_value)
    # end def uncaught_exception_handler
    sys.excepthook = uncaught_exception_handler

    # Instantiate application - not named "app" to avoid confusion with modules in app folder
    application = Quart(__name__)

    # Add error handler
    @application.errorhandler(Exception)
    def app_error_handler(error):
        """
        Handle uncaught exceptions in app routes
        See https://flask.palletsprojects.com/en/stable/errorhandling/

        :param: Exception err
        :rtype: dict
        """
        logger.error(request, 'Uncaught exception in app.', error)
        response = ApiResponse(500, str(error))

        return response.to_dict(), response.meta['status_code']
    # end def app_error_handler

    # Add routes
    api_routes(application)

    # Server config - see https://hypercorn.readthedocs.io/en/latest/how_to_guides/configuring.html
    internal_port = config.port_internal
    server_config = HypercornConfig()
    server_config.bind = [f"0.0.0.0:{internal_port}"] # listen on all IPs else not accessible outside Docker container
    server_config.loglevel = 'CRITICAL' # reduce log noise from Hypercorn

    # Start server programmatically instead of starting it via commandline
    # See https://hypercorn.readthedocs.io/en/latest/how_to_guides/api_usage.html
    logger.info(None, f"Server started listening at port {internal_port}.")
    asyncio.run(hypercorn_serve(application, server_config))
# end def main

# Run application
if __name__ == '__main__':
    main() # not placed in try/except as it is handled by uncaught_exception_handler()
# end if
