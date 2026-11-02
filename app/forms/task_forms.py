from flask_wtf import FlaskForm
from wtforms import DateField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
  title = StringField(
      'Title',
      validators=[
          DataRequired(message='Enter the title for your task'),
          Length(
              min=5,
              max=200,
              message='Title must be between 5 to 200 characters',
          ),
      ],
  )

  description = TextAreaField('Description', validators=[Optional()])

  due_date = DateField('Due Date', validators=[Optional()])


class UpdateTaskForm(FlaskForm):
  title = StringField(
      'Title',
      validators=[
          DataRequired(message='Enter the title for your task'),
          Length(
              min=5,
              max=200,
              message='Title must be between 5 to 200 characters',
          ),
      ],
  )

  description = TextAreaField('Description', validators=[Optional()])

  due_date = DateField('Due Date', validators=[Optional()])