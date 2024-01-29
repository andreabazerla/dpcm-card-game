import logging

class Logger:
    def __init__(self, log_file=None, log_level=logging.DEBUG):
        self.set_level(log_level)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.add_handler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.add_handler(file_handler)

    def set_level(self, level):
        self.logger.setLevel(level)

    def add_handler(self, handler):
        self.logger.addHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def clear_output(self):
        with open(f'{self.get_output_path()}/{self.get_file_name()}', 'r+') as file:
            file.truncate(0)