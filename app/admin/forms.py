from datetime import datetime

from flask import session, current_app
from flask_admin.form import SecureForm
from flask_sqlalchemy import DefaultMeta
from flask_wtf import FlaskForm
from flask_wtf.csrf import _FlaskFormCSRF
from wtforms import SubmitField, StringField, TextField, BooleanField, SelectMultipleField, SelectField, \
    DateTimeField, validators


class CustomSecureForm(SecureForm):
    class Meta(DefaultMeta):
        csrf_class = _FlaskFormCSRF
        csrf_context = session

        @property
        def csrf_secret(self):
            return current_app.config.get('WTF_CSRF_SECRET_KEY',
                                          current_app.secret_key)


class UserForm(FlaskForm):
    username = TextField()
    user_email = TextField()
    user_first_name = TextField()
    user_last_name = TextField()
    user_title = TextField()
    user_manager = TextField()
    user_is_admin = BooleanField('Admin User')
    user_groups = SelectMultipleField()
    btn = SubmitField('Edit User')


class PrinterForm(FlaskForm):
    printer_name = TextField(validators=[validators.DataRequired()])
    printer_model = TextField(validators=[validators.DataRequired()])
    printer_serial_number = TextField(validators=[validators.DataRequired()])
    printer_location = TextField(validators=[validators.DataRequired()])
    printer_ip_address = TextField(validators=[validators.IPAddress(ipv4=True,
                                                                    message="Please input a valid IP Address")])
    printer_contract = BooleanField()
    printer_type = SelectField(
        choices=[(1, 'Monochrome'), (2, 'Colour')],
        coerce=int,
        validators=[validators.Optional()]
    )
    edit_printer = SubmitField('Edit Printer')


class NewPrinterForm(FlaskForm):
    printer_name = StringField(
        validators=[validators.DataRequired()]
    )
    printer_model = StringField(
        validators=[validators.InputRequired(message="Please input a Printer Model")]
    )
    printer_serial_number = StringField(
        validators=[validators.InputRequired(message="Please input a Printer Serial Number")]
    )
    printer_location = StringField(
        validators=[validators.InputRequired(message="Please input a Printer Location")]
    )
    printer_ip_address = StringField(
        validators=[validators.IPAddress(ipv4=True,
                                         message="Please input a valid IP Address")]
    )
    printer_contract = SelectField(
        choices=[(1, 'Yes'), (2, 'No')],
        coerce=int,
        validators=[validators.Optional()]
    )
    printer_type = SelectField(
        choices=[(1, 'Monochrome'), (2, 'Colour')],
        coerce=int,
        validators=[validators.Optional()]
    )
    new_printer = SubmitField('New Printer')


class TonerReqForm(FlaskForm):
    printer_name = StringField()
    printer_model = StringField()
    printer_serial_number = StringField()
    printer_location = StringField()
    toner_request_date = DateTimeField('Toner Request Date', id='datepicker',
                                       format='%d-%m-%Y %H:%M:%S',
                                       default=datetime.utcnow())
    black_toner = BooleanField('Black Toner')
    cyan_toner = BooleanField('Cyan Toner')
    magenta_toner = BooleanField('Magenta Toner')
    yellow_toner = BooleanField('Yellow Toner')
    toner_request = SubmitField('Toner Request')


class TonerForm(FlaskForm):
    toner_req_number = StringField(render_kw={'readonly': True, 'disabled': True})
    toner_initiator_dn = StringField(render_kw={'readonly': True, 'disabled': True})
    toner_initiator_email = StringField(render_kw={'readonly': True, 'disabled': True})
    printer_name = StringField(render_kw={'readonly': True, 'disabled': True})
    printer_model = StringField(render_kw={'readonly': True, 'disabled': True})
    printer_serial_number = StringField(render_kw={'readonly': True, 'disabled': True})
    printer_location = StringField(render_kw={'readonly': True, 'disabled': True})
    black_toner = BooleanField('Black Toner', render_kw={'readonly': True, 'disabled': True})
    cyan_toner = BooleanField('Cyan Toner', render_kw={'readonly': True, 'disabled': True})
    magenta_toner = BooleanField('Magenta Toner', render_kw={'readonly': True, 'disabled': True})
    yellow_toner = BooleanField('Yellow Toner', render_kw={'readonly': True, 'disabled': True})
    toner_request = SubmitField('Toner Received')


class AccessRequestForm(FlaskForm):
    req_number = StringField()
    timestamp = StringField()
    initiator_dn = StringField()
    initiator_email = StringField()
    customer_dn = StringField()
    customer_email = StringField()
    mc_role = StringField()
    pms_role = StringField()
    pms_cashier = BooleanField()
    pms_sc = BooleanField()
    pos_role = StringField()
    email_type = StringField()
    email_license = StringField()
    email_addon = StringField()
    mdm_os = StringField()
    mdm_type = StringField()
    other_role = StringField()
    approver_hr = BooleanField()
    approver_hr_email = StringField()
    approver_hr_str = StringField()
    approver_acc = BooleanField()
    approver_acc_email = StringField()
    approver_acc_str = StringField()
    approver_gm = BooleanField()
    approver_gm_email = StringField()
    approver_gm_str = StringField()
    approver_it = BooleanField()
    approver_it_email = StringField()
    approver_it_str = StringField()
    req_edit = SubmitField('Edit Access Request')


class ApproverForm(FlaskForm):
    department_sn = SelectField(
        coerce=int,
        validators=[validators.Optional()]
    )
    approvers_eid = StringField()
    approvers_email = StringField()
    submit = SubmitField()


class DepartmentForm(FlaskForm):
    name = StringField()
    short_name = StringField()
    submit = SubmitField()


class RoleForm(FlaskForm):
    role_name = StringField()
    role_description = StringField()
    role_edit = SubmitField()
