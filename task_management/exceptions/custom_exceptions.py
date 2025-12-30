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

class NotAccessToCreationException(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id

class FieldNotFoundException(Exception):
    def __init__(self, field_id: str):
        self.field_id = field_id


class InvalidFieldConfigException(Exception):
    def __init__(
        self,
        field_type: str,
        invalid_keys: list | None = None,
        message: str | None = None
    ):
        self.field_type = field_type
        self.invalid_keys = invalid_keys

        if message:
            self.message = message
        elif invalid_keys:
            self.message = (
                f"Invalid config keys {invalid_keys} "
                f"for field type '{field_type}'."
            )
        else:
            self.message = f"Invalid config for field type '{field_type}'."

        super().__init__(self.message)


class InvalidFieldDefaultValueException(Exception):
    def __init__(
        self,
        field_type: str,
        default_value=None,
        message: str | None = None
    ):
        self.field_type = field_type
        self.default_value = default_value

        if message:
            self.message = message
        else:
            self.message = (
                f"Invalid default value '{default_value}' "
                f"for field type '{field_type}'."
            )

        super().__init__(self.message)


class AlreadyExistedTemplateNameException(Exception):
    def __init__(self, template_name: str):
        self.template_name = template_name


class DefaultTemplateAlreadyExistedException(Exception):
    def __init__(self, template_name: str):
        self.template_name = template_name