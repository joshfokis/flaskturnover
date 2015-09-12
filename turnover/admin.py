from flask import flash, redirect
from flask.ext.admin.contrib.sqla import ModelView, filters
from flask.ext.admin.form import rules
from flask.ext.admin import AdminIndexView, BaseView, expose
from werkzeug.security import generate_password_hash
from flask.ext.wtf import Form
from flask.ext.login import login_user, logout_user, current_user, login_required
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField, PasswordField, validators
from turnover import admin, db, lm
from .models import User, Role, EventsClient1, EventsClient2, EventsClient3, Alerts


class UserAdminView(ModelView):
    column_searchable_list = ('username',)
    column_sortable_list = ('username', 'role', 'active')
    column_exclude_list = ('pwd_hash',)
    form_excluded_columns = ('pwd_hash',)
    form_edit_rules = ('username', 'email', 'active')
    form_create_rules = ('username', 'password', 'email', 'role', 'active')
    # export_csv()
    # edit_form = AdminUserEditForm

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role.name == 'admin'

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        form_class.role = SelectField('Role', choices=[('3', 'Non Cleared'), ('2', 'Cleared'), ('1', 'Admin')])
        return form_class

    def create_model(self, form):
        model = self.model(
            form.username.data, form.password.data,
            form.email.data, form.role.data, form.active.data
        )
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()
        flash('User has been created.')

    # def update_model(self, form, model):

    #     form.populate_obj(model)
    #     model = self.model(
    #         form.username.data,
    #         form.email.data, form.role.data, form.active.data
    #     )
    #     self.session.add(model)
    #     self._on_model_change(form, model, False)
    #     self.session.commit()


class RoleAdminView(ModelView):
    column_list = ('id', 'name')

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role.name == 'admin'


class EventsClient1View(ModelView):
    column_labels = dict(posted='Timestamp', poster='User')
    column_list =('posted', 'poster', 'event')
    column_searchable_list = (EventsClient1.event, 'event')
    column_filters = ('poster', 'posted')
    column_default_sort = ('posted', True)
    # column_filters = (BooleanEqualFilter(EventsClient1.poster, 'poster'))

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role.name == 'admin'



class EventsClient2View(ModelView):
    column_labels = dict(posted='Timestamp', poster='User')
    column_list =('posted', 'poster', 'event')
    column_searchable_list = (EventsClient2.event, 'event')
    column_filters = ('poster', 'posted')
    column_default_sort = ('posted', True)

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role.name == 'admin'

class EventsClient3View(ModelView):
    column_labels = dict(posted='Timestamp', poster='User')
    column_list =('posted', 'poster', 'event')
    column_searchable_list = (EventsClient3.event, 'event')
    column_filters = ('poster', 'posted')
    column_default_sort = ('posted', True)

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role.name == 'admin'


class AlertAdminView(ModelView):
    column_searchable_list = (Alerts.details, 'details')
    column_filters = ('client', 'startdate', 'enddate', 'cleared')
    column_default_sort = ('startdate', True)

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role.name == 'admin'

admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))
admin.add_view(AlertAdminView(Alerts, db.session))
admin.add_view(EventsClient1View(EventsClient1, db.session, name='Client1', category='Clients'))
admin.add_view(EventsClient2View(EventsClient2, db.session, name='Client2', category='Clients'))
admin.add_view(EventsClient3View(EventsClient3, db.session, name='Client3', category='Clients'))

