from dataclasses import dataclass

@dataclass # https://docs.python.org/3/library/dataclasses.html
class ApiResponse:
    """
    Standardized format for responses from API endpoints
    """

    def __init__(self, status_code: int, error_message=None, data_object: dict=None):
        """
        Constructor

        :param int status_code: HTTP status code for response
        :param str|dict error_message: For error response, used as
            error message if string, else used for error object (should contain
            message key), set to '' for success response, defaults to None
        :param dict data_object: Data to be returned for success response,
            set to None for error response, defaults to None
        """

        if error_message is None or error_message == '':
            self.error = None
        elif isinstance(error_message, str):
            self.error = {
                'message': error_message
            }
        else:
            self.error = error_message
        # end if

        if self.error is not None:
            self.data = None
        else:
            self.data = data_object
        # end if

        self.meta = {
            'status_code': status_code,
            'version': 'v0.1.0'
        }
    # end def __init__

    def to_dict(self) -> dict:
        """
        Convert instance to dictionary for returning as response from a
        route handler

        :rtype: dict Dictionary containing top-level keys data, error, meta,
            each either a dictionary or None
        """

        return {
            'data': self.data,
            'error': self.error,
            'meta': self.meta,
        }
    # end def to_dict
# end class ApiResponse
