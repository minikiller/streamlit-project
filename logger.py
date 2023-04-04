import logging
import colorlog

# Configure the logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# # Create a colored log formatter
# formatter = colorlog.ColoredFormatter(
#     '%(log_color)s%(levelname)-8s%(reset)s %(message)s',
#     log_colors={
#         'DEBUG': 'cyan',
#         'INFO': 'green',
#         'WARNING': 'yellow',
#         'ERROR': 'red',
#         'CRITICAL': 'bold_red',
#     }
# )
formatter = colorlog.ColoredFormatter(
    (
        '%(log_color)s%(levelname)-5s%(reset)s '
        '%(yellow)s[%(asctime)s]%(reset)s'
        '%(white)s %(name)s %(funcName)s %(bold_purple)s:%(lineno)d%(reset)s '
        '%(log_color)s%(message)s%(reset)s'
    ),
    datefmt='%y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'bold_cyan',
        'WARNING': 'red',
        'ERROR': 'bg_bold_red',
        'CRITICAL': 'red,bg_white',
    }
)

# Create a console handler and add the formatter to it
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class Dog():
    myname=""

    def __init__(self) -> None:
        pass

    def click(self):
        logger.info("hello")
        print(self.myname)

dog=Dog()
dog.myname="hello"
dog.click()
