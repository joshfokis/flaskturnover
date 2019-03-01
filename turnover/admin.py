from flask import flash, redirect
from flask_admin.contrib.sqla import ModelView, filters
from flask_admin.form import rules
from flask_admin import AdminIndexView, BaseView, expose
from werkzeug.security import generate_password_hash
from flask_wtf import Form
from flask_login import login_user, logout_user, current_user, login_required
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, SelectField, PasswordField, validators
from turnover import admin, db, lm
from .models import User, Role, ClientEvents, Alerts


class UserAdminView(ModelView):
    """
    This creates the Admin Dashboard for the Application.
    """
    column_labels = dict(lastlogin='Last Login')
    column_searchable_list = ('username',)
    column_sortable_list = ('username', 'role', 'active', 'lastlogin')
    column_exclude_list = ('pwd_hash',)
    form_excluded_columns = ('pwd_hash',)
    form_edit_rules = ('username', 'email', 'active', 'role')
    form_create_rules = ('username', 'password', 'email', 'role', 'active')
    # export_csv()
    # edit_form = AdminUserEditForm

    def is_accessible(self):
        """
        This Function notes if the application is accessible and to which user roles.
        """
        return current_user.is_authenticated() and current_user.role.name == 'admin'

    def scaffold_form(self):
        """
        This Fucntion determines how the fields are viewed.
        """
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        return form_class

    def create_model(self, form):
        """
        Function creates a form for a model, This was a fix to convert a String to an INT.
        """
        roledata = None
        if str(form.role.data) == 'admin':
            roledata = 1
        elif str(form.role.data) == 'Cleared':
            roledata = 2

        model = self.model(
            form.username.data, form.password.data,
            form.email.data, form.active.data, roledata
        )
        #form.populate_obj(model)
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
    """
    This class creates the Role view.
    """
    column_list = ('id', 'name')

    def is_accessible(self):
        """
        This Function notes if the application is accessible and to which user roles.
        """
        return current_user.is_authenticated() and current_user.role.name == 'admin'


class EventsClient1View(ModelView):
    """
    This class creates the Event view for Client 1.
    """
    column_labels = dict(posted='Timestamp', poster='User')
    column_list =('posted', 'poster', 'event')
    column_searchable_list = (ClientEvents.event, 'event')
    column_filters = ('poster', 'posted')
    column_default_sort = ('posted', True)

    def is_accessible(self):
        """
        This Function notes if the application is accessible and to which user roles.
        """
        return current_user.is_authenticated() and current_user.role.name == 'admin'


class AlertAdminView(ModelView):
    """
    This creates the Alert view.
    """
    column_searchable_list = (Alerts.details, 'details')
    column_filters = ('client', 'startdate', 'enddate', 'cleared')
    column_default_sort = ('startdate', True)

    def is_accessible(self):
        """
        This Function notes if the application is accessible and to which user roles.
        """
        return current_user.is_authenticated() and current_user.role.name == 'admin'

"""
The below adds the database data to the views.
"""
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))
admin.add_view(AlertAdminView(Alerts, db.session))
admin.add_view(EventsClient1View(EventsClient1, db.session, name='Client1', category='Clients'))
admin.add_view(EventsClient2View(EventsClient2, db.session, name='Client2', category='Clients'))
admin.add_view(EventsClient3View(EventsClient3, db.session, name='Client3', category='Clients'))

