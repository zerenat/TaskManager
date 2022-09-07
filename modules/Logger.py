import os
import logging


class Log:
    def __init__(self, name, path):
        self.__name = name
        self.__path = path

    def log(self):
        pass


class Logger:
    def __init__(self):
        self.__logs = []

    def log(self, log_name: str, message: str, message_type: str):
        """
        Makes a log entry
        :param log_name: Name parameter of the target log
        :param message: Log entry
        :param message_type: Log entry type
        :return:
        """
        for log in self.__logs:
            if log_name == log.name:
                log.log()

    def add_log(self, log_name, log_folder_path):
        for log in self.__logs:
            if log_name == log.name:
                raise Exception(f"Log with given name already exists:\n{log_name}")
        if os.path.exists(log_folder_path):
            self.__logs.append(Log(log_name, log_folder_path))
        else:
            raise Exception(f"Invalid log path provided:\n{log_folder_path}")

    def remove_log(self, log_name):
        for log in self.__logs:
            if log_name == log.name:
                self.__logs.remove(log)


if __name__ == '__main__':
    pass