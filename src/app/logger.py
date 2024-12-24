import logging
import socket
import traceback
from app.config import config

class Logger:
    """
    Custom logger
    """

    def __init__(self):
        """
        Constructor
        """
        self.lumberjack = logging.getLogger(__name__) # not named instance/logger to avoid confusion
        self.lumberjack.setLevel(logging.DEBUG)

        # Create console handler with formatter and add to logger
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Log format from log() in https://github.com/zionsg/getmail/blob/master/src/App/Logger.php
        app_name = config.app_name.upper()
        console_formatter = logging.Formatter( # https://docs.python.org/2/library/logging.html#logging.Formatter
            # See https://docs.python.org/2/library/logging.html#logrecord-attributes
            # The rest of the format is handled by __format_message() as the request object is not available here
            f"[%(asctime)s.%(msecs)dZ] [%(levelname)s] [{app_name}] [%(pathname)s:%(lineno)d] %(message)s",
            '%Y-%m-%dT%H:%M:%S' # https://docs.python.org/3/library/time.html#time.strftime
        )

        console_handler.setFormatter(console_formatter)
        self.lumberjack.addHandler(console_handler)
    # end __init__

    def error(self, request, message, exception=None):
        """
        Log error message with optional exception

        :param quart.request request: Request
        :param str message: Message
        :param Exception exception: Exception if any
        :rtype: None
        """
        self.lumberjack.error(self.__format_message(request, message, exception))
    # end def exception

    def info(self, request, message):
        """
        Log informational message

        :param quart.request request: Request
        :param str message: Message
        :rtype: None
        """
        self.lumberjack.info(self.__format_message(request, message))
    # end def info

    def __format_message(self, request, message, exception=None):
        """
        Format message
        Log format from log() in https://github.com/zionsg/getmail/blob/master/src/App/Logger.php

        :param quart.request request: Request
        :param str message: Message
        :param Exception exception: Exception if any
        :rtype str
        """
        result = message
        if isinstance(exception, Exception):
            result = result + ' '.join(traceback.format_exception(exception)).replace('\n', '\\n')
        # end if

        result = f"[MSG {result}]"
        if request is None:
            result = result + ' [REQ null]'
        else:
            # See https://flask.palletsprojects.com/en/stable/api/#flask.Request
            result = result \
                + f" [REQ {request.remote_addr} {request.method} {request.content_type} {request.url}" \
                + f' "{request.user_agent}" no-request-id]'
        # end if

        env = config.env
        port_external = config.port_external
        port_internal = config.port_internal
        version = config.version
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        result = result + f" [SVR {ip}:{port_external},{port_internal} {env} {hostname} {version}]"

        return result
    # end def __format_message
# end class Logger

# Note this variable is exposed as a public property when this file is imported
logger = Logger()
