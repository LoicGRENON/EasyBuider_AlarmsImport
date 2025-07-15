from alarm_category import AlarmCategory


class CategorySettings:
    def __init__(self, name='', **kwargs):
        self.name = name
        self.alarm_category = AlarmCategory(**kwargs)

    def __repr__(self):
        return f"CategorySettings({self.name}, {self.alarm_category})"
