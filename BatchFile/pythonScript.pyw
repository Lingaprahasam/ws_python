import logging

if __name__ == '__main__':
    logging.basicConfig(filename="key_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

    while True:
        logging.info('Python Script')