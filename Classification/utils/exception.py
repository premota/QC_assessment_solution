import sys


def error_message_detail(error,error_detail:sys):
    """
    Generate a detailed error message including filename, line number, and error message.

    Args:
    error (Exception): The error that occurred.
    error_detail (sys): System information containing details about the error.

    Returns:
    str: Detailed error message including filename, line number, and error message.
    """
    
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message

    

class CustomException(Exception):
    """
    Custom exception class to handle errors and provide detailed error messages.

    Attributes:
    error_message (str): Detailed error message including filename, line number, and error message.
    """

    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    