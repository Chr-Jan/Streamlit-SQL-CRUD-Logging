import logging

def get_logger():
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    return logging.getLogger()