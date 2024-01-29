import logging

class Logger:
    def __init__(self, output_path, file_name, level=logging.INFO):
        self.output_path = output_path
        self.file_name = file_name
        self.level = level

    def get_output_path(self):
        return self.output_path

    def get_file_name(self):
        return self.file_name
    
    def get_level(self):
        return self.level
        
    def setup_logger(self, console=False, file=False):
        handlers = []

        if console:
            handlers.append(logging.StreamHandler())

        if file:
            handlers.append(logging.FileHandler(f'{self.get_output_path()}/{self.get_file_name()}'))

        logging.basicConfig(
            level=self.get_level(),
            format='%(asctime)s %(levelname)s %(message)s',
            handlers=handlers or [logging.NullHandler()]
        )

    def clear_output(self):
        with open(f'{self.get_output_path()}/{self.get_file_name()}', 'r+') as file:
            file.truncate(0)

    def info(self, message, *args, **kwargs):
        logging.info(message, *args, **kwargs)