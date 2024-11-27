"""
Module
"""

from datetime import datetime

@lambda _: _() # this decorator turns the function into an IIFE
def helper():
    """
    Common server-side helper functions
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
