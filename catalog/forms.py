from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Length
from app.validators import Unique, Exists
from catalog.models import Category, Item


class ItemForm(FlaskForm):
    name = StringField('name',
                       validators=[DataRequired(), Length(3, 240),
                                   Regexp('^[a-zA-Z0-9-_() ]*$',
                                          message="Should only contain\
                                            alphabets, numbers, _, -, ()")])

    description = TextAreaField('description',
                                validators=[DataRequired(), Length(100)])

    category_id = StringField('Category id',
                              validators=[DataRequired(),
                                          Exists(Category, 'hash_id')])

    def validate_name(form, field):
        if not form.id:
            check = Unique(Item, 'name', message='The item name is already \
                taken.')
        else:
            check = Unique(Item, 'name', form.id, message='The item name is \
                already taken.')

        check(form, field)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id', None)
        super().__init__(*args, **kwargs)
