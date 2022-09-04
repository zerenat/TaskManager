from modules.ConfigParser import ConfigParser

class TaskManager:
    def __init__(self, configuration):
        self.__configuration = configuration



if __name__ == '__main__':
    configuration = ConfigParser().get_config_as_dictionary(r'configuration/TaskManager_configuration.ini')
    task_manager = TaskManager(configuration)