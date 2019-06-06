from wtforms.validators import ValidationError


class Unique:
    """
    The field under validation must be unique on a given database table column.
    """
    def __init__(self, model, column, ignore_id=None, message=None):
        self.__model = model
        self.__column = column
        self.__ignore_id = ignore_id
        self.__message = 'The value given for {} is already taken'
        if message:
            self.__message = message

    def __call__(self, form, field):
        model = self.__model
        column = self.__column

        db_rows = model.query.filter(getattr(model, column) == field.data)

        if self.__ignore_id:
            if db_rows.filter_by(id != self.__ignore_id).count():
                raise ValidationError(self.__message.format(field.label.text))
        else:
            if db_rows.count():
                raise ValidationError(self.__message.format(field.label.text))
