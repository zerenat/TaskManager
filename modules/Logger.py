class Log:
    def __init__(self, name, path):
        self.__name = name
        self.__path = path

    def log(self):
        pass

    @property
    def name(self):
        return self.__name

class Logger:
    def __init__(self):
        self.__logs = []

    def log(self, log_name, message, message_type, ):
        for log in self.__logs:
            if log_name == log.name:
                log.log()
        # print(message)
