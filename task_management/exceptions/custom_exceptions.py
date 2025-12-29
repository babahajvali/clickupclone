class UserNotFoundException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id


class TemplateNotFoundException(Exception):
    def __init__(self, template_id: str):
        self.template_id = template_id

class UnexpectedFieldTypeFoundException(Exception):
    def __init__(self, field_type: str):
        self.field_type = field_type


class FieldNameAlreadyExistsException(Exception):
    def __init__(self, field_name: str):
        self.field_name = field_name


class FieldOrderAlreadyExistsException(Exception):
    def __init__(self, field_order: int):
        self.field_order = field_order

class NotAccessToCreateFieldException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

class FieldNotFoundException(Exception):
    def __init__(self, field_id: str):
        self.field_id = field_id