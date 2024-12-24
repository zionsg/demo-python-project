import os

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

# Note this variable is exposed as a public property when this file is imported
config = Config()
