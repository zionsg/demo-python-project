from datetime import datetime

@lambda _: _() # decorator turns function into an IIFE (Immediately Invoked Function Expression)
def helper(): # this module is written as an IIFE for reference, instead of like src/app/logger.py
    """
    Get initialized helper

    Usage:
        from app.helper import helper  # path relative to src/index.py
        result = helper.timestamp() # helper() not needed due to IIFE

    :rtype: Helper Initialized instance
    """

    class Helper:
        """
        Common server-side helper functions
        """

        def timestamp(self, seconds_only=False):
            """
            Get current timestamp

            :param bool seconds_only: Whether to return up to seconds portion,
                i.e. omit microseconds, defaults to False.
            :rtype: str Timestamp in ISO 8601 format
            """
            return datetime.now().strftime(
                '%Y-%m-%dT%H:%M:%SZ' if seconds_only else '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        # end def timestamp
    # end class Helper

    # Return public interface of IIFE, don't pollute global namespace with internal class/func/var
    return Helper() # only 1 instance will be created as the function is immediately invoked
# end def helper
