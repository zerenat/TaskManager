import queue
import threading
import time
import traceback
from modules.ConfigParser import ConfigParser
from modules.Logger import Logger
from modules.Time import Time
import subprocess
import os


class TaskManager:
    def __init__(self, configuration_file_path):
        self.__active = True
        self.__configuration_file_path = configuration_file_path
        self.__config_parser = ConfigParser()
        self.__logger = Logger()
        self.__time = Time()
        self.__last_run_time = None
        self.__completed_runs = []
        self.__active_tasks = []
        self.__task_queue = queue.Queue(maxsize=25)
        self.__sub_worker = None

    def run_tool(self):
        try:
            if not self.__sub_worker:
                self.__sub_worker = threading.Thread(target=self.run_sub_process, daemon=True)
                self.__sub_worker.start()
            attributes = self.__load_configuration()
            tasks = eval(attributes['tasks']['tasks'])

            time_object = self.__time.get_time_map()
            current_time_tuple = (time_object['hour'], time_object['minute'])
            if current_time_tuple not in self.completed_runs:
                self.completed_runs = current_time_tuple
                self.__last_run_time = current_time_tuple
            for task in tasks:
                try:

                    # TESTING
                    self.__task_queue.put(task)
                    # =======

                    execution_time = task['execution_times']
                    if execution_time[0] == time_object['hour']:
                        if execution_time[1] == time_object['minute']:
                            self.__task_queue.put(task)
                except KeyError as e:
                    self.__logger.log_operation(f"Failed to parse configuration time for:\n{str(task)} \n{str(e)}",
                                                "error")
                    time.sleep(2)
                except TypeError as e:
                    self.__logger.log_operation(f"Failed to parse configuration time for:\n{str(task)} \n{str(e)}",
                                                "error")
                    time.sleep(2)
            while self.__time.get_time_map()['minute'] == current_time_tuple[1]:

                time.sleep(10)
            self.run_tool()
        except Exception as e:
            self.__logger.log_operation(f"Error running the TaskManager: \n{str(e)}", "error")
            time.sleep(2)

    def run_sub_process(self):
        def __do_work(task_name, task_path):
            """
            The function runs a subprocess
            :param task_name: Name of the task
            :param task_path: Path to the executable bat/ exe/ etc
            """
            print("Running task:", task_name)
            subprocess.run(task_path)
            self.__manage_active_tasks({'task_name': task_name}, True)
        try:
            while True:
                if not self.__task_queue.empty():
                    task = self.__task_queue.get()
                    task_name = task['task_name']

                    # Check if task is already active and skip the relaunch if true
                    task_already_active = False
                    for active_task in self.active_tasks:
                        if task['task_name'] == active_task['task_name']:
                            task_already_active = True
                            break
                    if task_already_active:
                        continue

                    task_path = task['task_path']
                    thread = threading.Thread(target=__do_work, args=(task_name, task_path), daemon=True)
                    thread.start()
                    self.__manage_active_tasks({'task_name': task_name, 'task_thread': thread})

                    for item in self.active_tasks:
                        print(item)

                else:
                    time.sleep(5)
        except KeyError as e:
            self.__logger.log_operation(f"Failed to parse task information \n{str(e)}", "error")
            time.sleep(2)
        except Exception:
            traceback.print_exc()
            time.sleep(2)



    def __load_configuration(self, section: str = None):
        try:
            configuration = self.__config_parser.get_config_as_dictionary(self.__configuration_file_path)
            return configuration if section is None else configuration[section]
        except FileNotFoundError:
            raise FileNotFoundError("Failed to read the configuration file.")
        except KeyError:
            raise KeyError("Configuration file format unknown to the tool.")
        except Exception:
            raise



    def toggle_active(self):
        self.__active = False if self.__active is True else True

    @property
    def active_tasks(self):
        return self.__active_tasks

    def __manage_active_tasks(self, value: dict, remove: bool = False):
        if not remove:
            self.active_tasks.append(value)
        else:
            for task in self.active_tasks:
                try:
                    if task['task_name'] == value['task_name']:
                        self.active_tasks.remove(task)
                except KeyError:
                    continue

    @property
    def completed_runs(self):
        return self.__completed_runs

    @completed_runs.setter
    def completed_runs(self, value):
        if not value:
            self.completed_runs.clear()
        else:
            self.completed_runs.append(value)



if __name__ == '__main__':
    config_parser = ConfigParser()
    task_manager = TaskManager('configuration/TaskManager_configuration.ini')
    task_manager.run_tool()
