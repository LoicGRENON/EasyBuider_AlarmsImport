from alarm_category import AlarmCategory


class CategorySettings:
    def __init__(self, name='', **kwargs):
        self.name = name
        self.alarm_category = AlarmCategory(**kwargs)
