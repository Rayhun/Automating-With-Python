import logging

def set_custom_info(filename):
    logging.basicConfig(
        filename=filename, level=logging.INFO
    )

def report(e:Exception):
    logging.exception(str(e))
