from enum import Enum


class FieldTypes(Enum):
    DROPDOWN = "DROPDOWN"
    USER = "USER"
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATE = "DATE"
    CHECKBOX = "CHECKBOX"
    EMAIL = "EMAIL"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value) for member in cls]

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]


class Role(Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    GUEST = "GUEST"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value) for member in cls]

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]


class Permissions(Enum):
    FULL_EDIT = "FULL_EDIT"
    COMMENT = "COMMENT"
    VIEW = "VIEW"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value) for member in cls]

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]


class ViewType(Enum):
    TABLE = "TABLE"
    CALENDER = "CALENDER"
    BOARD = "BOARD"
    DASHBOARD = "DASHBOARD"
    LIST = "LIST"
    GANTT = "GANTT"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value) for member in cls]

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]


class Visibility(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value) for member in cls]

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

    @classmethod
    def get_list_of_tuples(cls):
        return [(member.value, member.value) for member in cls]

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]
