from wtforms.validators import ValidationError


class Unique:
    """
    The field under validation must be unique on a given database table column.
    params:
    model(class): sqlalchemy database model.
    column(str): The column name to check if the value exists.
    ignore_id(int): The row id to be ignored for unique check. Can used for
    validating data on update or patch methods.
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
            if db_rows.filter(getattr(model, 'id')
                              != self.__ignore_id).count():
                raise ValidationError(self.__message.format(field.label.text))
        else:
            if db_rows.count():
                raise ValidationError(self.__message.format(field.label.text))
