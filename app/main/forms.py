import datetime
from operator import itemgetter

from datetime import date

from flask_wtf import FlaskForm, Form
from wtforms import SubmitField, SelectField, StringField, TextField, BooleanField, SelectMultipleField, \
    TextAreaField, validators, PasswordField
from wtforms.validators import Length, DataRequired, regexp, ValidationError, Optional, EqualTo
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea


class PostForm(FlaskForm):
    author = StringField('Author',
                         render_kw={'disabled': ''})
    description = StringField('Description',
                              default='',
                              validators=[Length(max=25)])
    body = StringField('Post Body',
                       default='',
                       validators=[Length(max=255)],
                       widget=TextArea(),
                       id='body')
    body_count = StringField(id='body_count',
                             default="250 characters remaining")
    submit = SubmitField('New Post')


class EditProfileForm(FlaskForm):
    email = StringField('Email:',
                        id='email_edit')
    about_me = StringField('About me:',
                           default='',
                           validators=[Length(max=250)],
                           widget=TextArea(),
                           id='about_me_edit')
    about_me_count = StringField(id='about_me_count')
    submit_edit = SubmitField('Save Details')
    change_pwd = SubmitField('Change Password')


class AccessRequestForm(FlaskForm):

    initiator = TextField(
        'Initiator',
        description="Request initiator EID"
    )

    initiator_email = TextField(
        'Initiator Email',
        description="Request initiator Email Address"
    )

    customer = StringField(
        'Customer',
        description="Customer EID",
        validators=[regexp(regex=r'[A-Za-z]{5}[0-9]{3}', message='Please input a valid EID')]
    )

    customer_email = TextField(
        'Customer Email',
        description="Customer Email Address"
    )

    customer_ou = TextField(
        'Customer OU',
        description="User's MARSHA CODE"
    )

    customer_title = TextField(
        'Customer Title',
        description="Users' Job Title"
    )

    dates = DateField('Date',
                      id='datepicker',
                      format='%Y-%m-%d',
                      default=date.today(),
                      description="Please select a valid date using the format 'dd/mm/yyyy'",
                      validators=[DataRequired('Date is required')])

    # default = list(map(itemgetter(0), pos_choices))[-1],
    # default = list(pos_choices)[-1],
    mc_boolean = BooleanField('Materials Control')
    materials_control = SelectField('Materials Control Roles',
                                    coerce=int,
                                    description="Please click 'Materials Control' check-box to select a MC Role",
                                    validators=[validators.Optional()])

    pms_boolean = BooleanField('OPERA PMS')
    pms = SelectField('PMS Roles',
                      description="Please click 'OPERA PMS' check-box to select a OPERA PMS Role",
                      coerce=int,
                      validators=[validators.Optional()])

    pms_cashier = SelectField('OPERA CASHIER',
                              choices=[(1, 'Yes'), (2, 'No')],
                              default=2,
                              coerce=int,
                              description="Please select Yes or No",
                              validators=[validators.Optional()])

    pms_sc = SelectField('OPERA S&C OWNER',
                         choices=[(1, 'Yes'), (2, 'No')],
                         default=2,
                         coerce=int,
                         description="Please select Yes or No",
                         validators=[validators.Optional()])

    simphony_boolean = BooleanField('Simphony')
    simphony = SelectField('Simphony Roles',
                           coerce=int,
                           description="Please click 'Simphony' check-box to select a POS Simphony Role",
                           validators=[validators.Optional()])

    shares_boolean = BooleanField('Shared Folders')
    shares = SelectMultipleField('Shared Folders',
                                 description="Please click 'Shared Folders' check-box and " +
                                             "keep CTRL pressed to select multiple items",
                                 coerce=int,
                                 validators=[validators.Optional()])

    email_type_boolean = BooleanField('Email')
    email_type = SelectField('Email Type',
                             coerce=int,
                             description="Please select a email Type",
                             validators=[validators.Optional()])

    email_licenses = SelectField('Email Licenses',
                                 coerce=int,
                                 description="Please select a email License",
                                 validators=[validators.Optional()])

    email_addons_boolean = BooleanField('Email Add-ons')
    email_addons = SelectField('Email Add-ons',
                               coerce=int,
                               description="Please select a email Add-On",
                               validators=[validators.Optional()])

    mdm_os_boolean = BooleanField('Mobile Device Management')
    mdm_os = SelectField('Mobile Device OS',
                         description='Please select device OS',
                         coerce=int,
                         validators=[validators.Optional()])
    mdm_type = SelectField('Mobile Device Type',
                           description='Please select a device Type',
                           coerce=int,
                           validators=[validators.Optional()])

    other = TextField('Other Requests',
                      description='Fill this field if you have other requests',
                      validators=[validators.Optional()])

    submit = SubmitField('Request')


class SimphonyForm(FlaskForm):

    def validate_number(self, field):
        if self.submit.data:
            return True
        elif self.add.data:
            try:
                value = float(field.data)
                return True
            except:
                raise ValidationError(field.label.text + ' field must have a valid number')

    def validate_fields(self, field):
        if self.submit.data:
            return True
        elif self.add.data:
            # print(field.name, field.data == '', field.label.text)
            if len(field.data) == 0 or field.data == '':
                raise ValidationError(field.label.text + " field cannot be empty!")

    rvc = StringField('Revenue Center', validators=[validate_fields])
    type = SelectField('Add/Mod', coerce=str,
                       choices=[('Add', 'Add'), ('Mod', 'Mod')],
                       default='Add')
    item_name = StringField('Item Name', validators=[validate_fields])
    major_group = StringField('Major group', validators=[validate_fields])
    slu = StringField('SLU', validators=[validate_fields])
    remarks = StringField('Remarks', validators=[Optional()])
    selling_price = StringField('Selling Price', validators=[validate_number])
    cost_price = StringField('Cost Price', validators=[validate_number])
    cost_percent = StringField('Cost Percentage', validators=[validate_number])
    add = SubmitField('Add')
    submit = SubmitField('Place Request')
    cancel = SubmitField('Cancel Request')


