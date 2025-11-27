from datetime import datetime

class TaskModel:
    """
    Task model with anti-pattern: getter/setter methods
    Anti-pattern: gci7-python-avoid-creating-getter-and-setter-methods-in-classes
    Should use @property decorator instead
    """

    def __init__(self, id=None, title="", description="", status="todo", user_id=None, priority=1):
        self._id = id
        self._title = title
        self._description = description
        self._status = status
        self._user_id = user_id
        self._priority = priority
        self._created_at = datetime.now()

    # Anti-pattern: Using getter methods instead of @property
    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_status(self):
        return self._status

    def get_user_id(self):
        return self._user_id

    def get_priority(self):
        return self._priority

    # Anti-pattern: Using setter methods instead of @property
    def set_title(self, title):
        self._title = title

    def set_description(self, description):
        self._description = description

    def set_status(self, status):
        self._status = status

    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_priority(self, priority):
        self._priority = priority

    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "status": self._status,
            "user_id": self._user_id,
            "priority": self._priority,
            "created_at": self._created_at.isoformat()
        }
