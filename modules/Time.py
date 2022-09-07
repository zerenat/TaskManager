import datetime


class Time:
    def __init__(self):
        self.__day_map = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def get_time_map(self, day_offset: int = None):
        if day_offset:
            current_time = datetime.datetime.now() + datetime.timedelta()
        else:
            current_time = datetime.datetime.now()
        time_map = {'date': current_time.date(),
                    'day_of_week_index': current_time.weekday(),
                    'day_of_week': self.__day_map[current_time.weekday()],
                    'hour': current_time.hour,
                    'minute': current_time.minute,
                    'second': current_time.second}

        return time_map
