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

        def dict_to_comma_delimited(self, source_dict: dict) -> str:
            """
            Convert dictionary to comma-delimited string

            Each key-value pair in the dictionary will be turned into a colon-delimited tuple.

            Colon is used as the secondary delimiter for the tuples instead of semi-colon as the
            bottom half of the semi-colon looks like a comma which can cause confusion, even though
            the semi-colon is grammatically more suitable.

            :param dict source_dict: Dictionary to convert
            :return: E.g.: { a:1, b:'test' } becomes 'a:1,b:test'
            :rtype: str
            """
            if not isinstance(source_dict, dict) or source_dict is None:
                return ''
            # end if

            result_list = []
            for _, (key, value) in enumerate(source_dict.items()): # _ used for index to prevent Pylint unused-variable
                result_list.append(f"{key}:{value}")
            # end for source_dict

            return ','.join(result_list)
        # end def dict_to_comma_delimited

        def timestamp(self, seconds_only: bool=False) -> str:
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
