from datetime import datetime

@lambda _: _() # decorator turns function into an IIFE (Immediately Invoked Function Expression)
def helper():
    """
    Common server-side helper functions

    Usage:
        from app.helper import helper  # path relative to src/index.py
        result = helper['timestamp']() # helper() not needed due to IIFE

    :rtype: dict Dictionary containing public methods to call
    """

    def timestamp(seconds_only=False):
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

    # Return public interface of IIFE, does not pollute global namespace with internal vars/funcs
    return {
        'timestamp': timestamp,
    }
# end def helper
