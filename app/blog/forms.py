from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, \
    SelectMultipleField, FileField
from wtforms.validators import Optional, DataRequired, StopValidation, length

from config import Config


class BlogEditor(FlaskForm):
    title = StringField("Title", validators=[Optional(), length(max=128)])
    description = StringField("Description", validators=[Optional(), length(max=256)])
    body = TextAreaField("Text", validators=[Optional()])
    tags = SelectMultipleField("Tags",
                               choices=[])
    image = FileField("Select File")
    upload = SubmitField("Upload File", render_kw={})
    submit = SubmitField("Save Post", render_kw={})
    cancel = SubmitField("Dispose Post", render_kw={})

    @staticmethod
    def allowed_image_filesize(filesize):

        if int(filesize) <= Config.FILEUPLOAD_MAX_CONTENT_LENGTH:
            return True
        else:
            return False


class FileUploader(FlaskForm):
    image = FileField("Select File")
    submit = SubmitField("Upload File")

    @staticmethod
    def allowed_image_filesize(filesize):

        if int(filesize) <= Config.FILEUPLOAD_MAX_CONTENT_LENGTH:
            return True
        else:
            return False