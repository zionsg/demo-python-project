import os

@lambda _: _() # decorator turns function into an IIFE (Immediately Invoked Function Expression)
def config():
    """
    Get initialized config

    Usage:
        from app.config import config  # path relative to src/index.py
        print(config.internal_port)

    :rtype: Config Initialized instance
    """

    class Config:
        """
        Application configuration resolved from environment variables
        """

        def __init__(self):
            """
            Constructor
            """
            self.env = os.getenv('DEMO_ENV', 'production')
            self.port_external = int(os.getenv('DEMO_PORT_EXTERNAL', '10000'))
            self.port_internal = int(os.getenv('DEMO_PORT_INTERNAL', '9000'))
            self.app_name = os.getenv('DEMO_APP_NAME', 'DEMO')
            self.debug = (1 == int(os.getenv('DEMO_DEBUG', '0')))
            self.version = 'v0.1.0'
        # end def __init__
    # end class Config

    # Return public interface of IIFE, don't pollute global namespace with internal class/func/var
    return Config() # only 1 instance will be created as the function is immediately invoked
# end def config
