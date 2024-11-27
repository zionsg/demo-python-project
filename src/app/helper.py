"""
Module
"""

from datetime import datetime

@lambda _: _() # decorator turns function into an IIFE (Immediately Invoked Function Expression)
def helper():
    """
    Common server-side helper functions

    Usage:
        from app.helper import helper  # path relative to src/index.py
        result = helper['timestamp']() # helper() not needed due to IIFE

    :rtype: dict
    """

    def timestamp():
        """
        Return current timestamp in ISO 8601 format

        :rtype: str
        """

        return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # end def timestamp

    # Return public interface
    return {
        'timestamp': timestamp,
    }
# end def module
