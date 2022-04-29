import logging


def clear():
    print('\n' * 50)


class Utils:
    """
        Class containing general utilities: functions and data structures
    """
    ''' 
        Log levels:

        INFO: Confirmation that things are working as expected.
        DEBUG: Detailed information, typically of interest only when diagnosing problems.
        WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
        ERROR: Due to a more serious problem, the software has not been able to perform some function.
        CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
        '''
    log_levels = None

    def __init__(self):
        self.log_levels = {
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        self.supported_browsers = [
            'chrome'
        ]

        # class name of the first result on a google search
        self.first_classname = 'iUh30'
