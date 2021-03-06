from wtforms.validators import ValidationError


class Exists:
    """
    The field under validation must exist on a given database table column.
    params:
    model(class): sqlalchemy database model.
    column(str): The column name to check if the value exists.
    message(str): Custom error message. The str part {} is formatted with the
    input field name.
    """
    def __init__(self, model, column, message=None):
        self.__model = model
        self.__column = column
        self.__message = 'The given {} does not exist.'
        if message:
            self.__message = message

    def __call__(self, form, field):
        values = []
        model = self.__model
        column = self.__column

        for value in model.query.all():
            values.append(getattr(value, column))

        if field.data not in values:
            raise ValidationError(self.__message.format(field.label.text))
