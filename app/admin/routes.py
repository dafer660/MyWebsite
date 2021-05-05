from datetime import datetime

from flask import render_template, redirect, url_for, request, abort, flash
from flask_security import roles_required, login_required, current_user

from app import login_manager, db, security
from app.admin import bp
from app.admin.forms import UserForm, NewPrinterForm

from app.models.user import User
from app.models.posts import Post


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()

        if not current_user.confirmed and request.endpoint[:5] != 'auth':
            return redirect(url_for('auth.login'))

        if not request.endpoint[:5] != 'auth':
            return redirect(url_for('auth.login'))

        db.session.commit()


@bp.route('/admin', methods=['GET'])
@bp.route('/admin/', methods=['GET'])
@login_required
@roles_required('admin')
def index():

    return render_template('admin/index.html')


@bp.route('/admin/user', methods=['GET'])
@login_required
@roles_required('admin')
def user():
    users = User.get_users()
    return render_template('admin/../templates/00 - unused/users_list.html', users=users)


@bp.route('/admin/user/<id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def user_detail(id):
    user = User.get_user_by_id(current_user.id)

    if user is None:
        return abort(404)

    form = UserForm()

    if request.method == 'GET':
        form.username.data = user.username
        form.username.render_kw = {'readonly': True}
        form.user_email.data = user.email
        form.user_email.render_kw = {'readonly': True}
        form.user_is_admin.data = user.admin
        try:
            initial_list = list(user.groups.split(',')[:-1])
            group_choices = [(x + 1, initial_list[x]) for x in range(len(initial_list))]
            form.user_groups.choices = group_choices
        except:
            form.user_groups.choices = [("", "")]

        form.user_groups.render_kw = {'readonly': True, 'disabled': True, 'hidden': True}

    if form.validate_on_submit():
        user.admin = form.user_is_admin.data
        db.session.commit()
        return redirect(url_for('admin.user'))

    return render_template('admin/../templates/00 - unused/users_detail.html', user=user, form=form)


@bp.route('/admin/roles')
@login_required
@roles_required('admin')
def roles_list():
    # TODO
    users = User.get_users()
    return render_template('admin/../templates/00 - unused/users_list.html', users=users)


@bp.route('/admin/posts')
@login_required
@roles_required('admin')
def posts_list():
    # TODO
    posts = Post.query_posts()
    return render_template('admin/../templates/00 - unused/posts_list.html', posts=posts)


@bp.route('/admin/printer_new', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def printer_new():

    form = NewPrinterForm()
    if form.validate_on_submit():

        printer_contract_form = dict(form.printer_contract.choices).get(form.printer_contract.data)
        printer_type = dict(form.printer_type.choices).get(form.printer_type.data)

        if printer_contract_form == 'Yes':
            printer_contract = True
        else:
            printer_contract = False

        #printer_status = check_ping(form.printer_ip_address.data)

        # new_printer = Printer(
        #     printer_name=form.printer_name.data,
        #     printer_model=form.printer_model.data,
        #     printer_serial_number=form.printer_serial_number.data,
        #     printer_location=form.printer_location.data,
        #     printer_ip_address=form.printer_ip_address.data,
        #     printer_contract=printer_contract,
        #     printer_type=printer_type,
        #     printer_status=printer_status
        # )

        # db.session.add(new_printer)
        # db.session.commit()

        return redirect(url_for('admin.printers'))

    return render_template('admin/../templates/00 - unused/printers_new.html', form=form)


@login_required
@roles_required('admin')
@bp.route('/admin/toner_requests', methods=['GET'])
def printer_toners():
    try:
        toners = None
    except:
        toners = ''

    if toners is None:
        abort(404)

    return render_template('admin/index.html', toners=toners)


@login_required
@roles_required('admin')
@bp.route('/admin/toner_request/<id>', methods=['GET', 'POST'])
def printer_toner_request(id):
    #TODO
    print("TODO")

