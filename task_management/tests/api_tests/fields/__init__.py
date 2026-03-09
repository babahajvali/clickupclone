from task_management.tests.test_utils import GraphQLBaseTestCase


class BaseCreateField(GraphQLBaseTestCase):
    QUERY = """
    mutation CreateField($params: CreateFieldInputParams!) {
      createField(params: $params) {
        ... on FieldType {
          __typename
          fieldId
          fieldType
          description
          templateId
          fieldName
          isDeleted
          order
          config
          isRequired
          createdBy
        }
        ... on TemplateNotFoundType {
          __typename
          templateId
        }
        ... on FieldNameAlreadyExistsType {
          __typename
          fieldName
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
        ... on InvalidFieldConfigType {
          __typename
          fieldType
          invalidKeys
          invalidConfigMessage: message
        }
        ... on EmptyFieldNameType {
          __typename
          fieldName
        }
        ... on MissingFieldConfigType {
          __typename
          fieldType
        }
        ... on DropdownOptionsMissingType {
          __typename
          fieldType
        }
        ... on TextDefaultValueExceedsMaxLengthType {
          __typename
          textDefaultMessage: message
        }
        ... on NumberDefaultValueBelowMinimumType {
          __typename
          numberMinDefaultMessage: message
        }
        ... on NumberDefaultValueAboveMaximumType {
          __typename
          numberMaxDefaultMessage: message
        }
        ... on DropdownDefaultValueNotInOptionsType {
          __typename
          dropdownDefaultMessage: message
        }
        ... on MaxValueLessThanMinValueType {
          __typename
          fieldType
          maxLessThanMinMessage: message
        }
      }
    }
    """


class BaseUpdateField(GraphQLBaseTestCase):
    QUERY = """
    mutation UpdateField($params: UpdateFieldInputParams!) {
      updateField(params: $params) {
        ... on FieldType {
          __typename
          fieldId
          fieldType
          description
          templateId
          fieldName
          isDeleted
          order
          config
          isRequired
          createdBy
        }
        ... on FieldNotFoundType {
          __typename
          fieldId
        }
        ... on DeletedFieldType {
          __typename
          fieldId
        }
        ... on FieldNameAlreadyExistsType {
          __typename
          fieldName
        }
        ... on EmptyFieldNameType {
          __typename
          fieldName
        }
        ... on MissingFieldConfigType {
          __typename
          fieldType
        }
        ... on DropdownOptionsMissingType {
          __typename
          fieldType
        }
        ... on InvalidFieldConfigType {
          __typename
          fieldType
          invalidKeys
          invalidConfigMessage: message
        }
        ... on TextDefaultValueExceedsMaxLengthType {
          __typename
          textDefaultMessage: message
        }
        ... on NumberDefaultValueBelowMinimumType {
          __typename
          numberMinDefaultMessage: message
        }
        ... on NumberDefaultValueAboveMaximumType {
          __typename
          numberMaxDefaultMessage: message
        }
        ... on DropdownDefaultValueNotInOptionsType {
          __typename
          dropdownDefaultMessage: message
        }
        ... on MaxValueLessThanMinValueType {
          __typename
          fieldType
          maxLessThanMinMessage: message
        }
        ... on NothingToUpdateFieldType {
          __typename
          fieldId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
      }
    }
    """


class BaseDeleteField(GraphQLBaseTestCase):
    QUERY = """
    mutation DeleteField($params: DeleteFieldInputParams!) {
      deleteField(params: $params) {
        ... on FieldType {
          __typename
          fieldId
          fieldType
          description
          templateId
          fieldName
          isDeleted
          order
          config
          isRequired
          createdBy
        }
        ... on FieldNotFoundType {
          __typename
          fieldId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
      }
    }
    """


class BaseReorderField(GraphQLBaseTestCase):
    QUERY = """
    mutation ReorderField($params: ReorderFieldInputParams!) {
      reorderField(params: $params) {
        ... on FieldType {
          __typename
          fieldId
          fieldType
          description
          templateId
          fieldName
          isDeleted
          order
          config
          isRequired
          createdBy
        }
        ... on FieldNotFoundType {
          __typename
          fieldId
        }
        ... on DeletedFieldType {
          __typename
          fieldId
        }
        ... on TemplateNotFoundType {
          __typename
          templateId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
        ... on InvalidOrderType {
          __typename
          order
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
      }
    }
    """


class BaseSetFieldValue(GraphQLBaseTestCase):
    QUERY = """
    mutation UpdateFieldValue($params: SetFieldValuesInputParams!) {
      updateFieldValue(params: $params) {
        ... on FieldValueType {
          __typename
          id
          taskId
          fieldId
          value
        }
        ... on TaskNotFoundType {
          __typename
          taskId
        }
        ... on DeletedTaskType {
          __typename
          taskId
        }
        ... on FieldNotFoundType {
          __typename
          fieldId
        }
        ... on DeletedFieldType {
          __typename
          fieldId
        }
        ... on UserNotWorkspaceMemberType {
          __typename
          userId
        }
        ... on ModificationNotAllowedType {
          __typename
          userId
        }
        ... on TextValueExceedsMaxLengthType {
          __typename
          message
        }
        ... on InvalidNumberFieldValueType {
          __typename
          message
        }
        ... on NumberValueBelowMinimumType {
          __typename
          message
        }
        ... on NumberValueExceedsMaximumType {
          __typename
          message
        }
        ... on DropdownOptionNotAllowedType {
          __typename
          message
        }
      }
    }
    """


class BaseGetField(GraphQLBaseTestCase):
    QUERY = """
    query GetFields($params: GetFieldsInputParams!) {
      getFields(params: $params) {
        ... on FieldsType {
          __typename
          fields {
            fieldId
            fieldType
            description
            templateId
            fieldName
            isDeleted
            order
            config
            isRequired
            createdBy
          }
        }
        ... on InvalidFieldIdsType {
          __typename
          fieldIds
        }
      }
    }
    """


class BaseGetTemplateFields(GraphQLBaseTestCase):
    QUERY = """
    query GetTemplateFields($params: GetFieldsForTemplateInputParams!) {
      getTemplateFields(params: $params) {
        ... on FieldsType {
          __typename
          fields {
            fieldId
            fieldType
            description
            templateId
            fieldName
            isDeleted
            order
            config
            isRequired
            createdBy
          }
        }
        ... on TemplateNotFoundType {
          __typename
          templateId
        }
      }
    }
    """
