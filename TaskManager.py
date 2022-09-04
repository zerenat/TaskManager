import logging
import datetime
from modules.ConfigParser import ConfigParser


class TaskManager:
    def __init__(self, configuration_file_path):
        self.__active = True
        self.__configuration_file_path = configuration_file_path
        self.__config_parser = ConfigParser()

    def run_tool(self):
        try:
            attributes = self.__load_configuration()
            print()
        except Exception as e:
            self.__log_operation(message="".join(("Error running the TaskManager: \n", str(e))))

    def __get_time(self):
        pass

    def __load_configuration(self):
        try:
            configuration = self.__config_parser.get_config_as_dictionary(self.__configuration_file_path)
            return {configuration['general']}
        except FileNotFoundError:
            raise FileNotFoundError("Failed to read the configuration file.")
        except KeyError:
            raise KeyError("Configuration file format unknown to the tool.")
        except Exception:
            raise

    def __log_operation(self, message):
        print(message)

    def toggle_active(self):
        is_nice = True
        is_nice = False if is_nice else False
        # self.__active = False if self.__active is True else self.__active = True


if __name__ == '__main__':
    config_parser = ConfigParser()
    task_manager = TaskManager('configuration/TaskManager_configuration.ini')
    task_manager.run_tool()
