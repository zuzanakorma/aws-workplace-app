from flask import redirect, url_for, request, abort
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user



# class UserView(ModelView):
#     form_columns = ["firstname", "lastname", "email", "password", "member", "roles"]
class UserView(ModelView):
    form_columns = ["firstname", "lastname", "email", "password", "member"]
    column_labels = dict(member='Department')

# class DepartmentView(ModelView):
#     form_columns = ["name"]

class DepartmentView(ModelView):
    form_columns = ["name"]
    column_labels = dict(name='Department')


class MyModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
              # login
                return redirect(url_for('main.workplace', next=request.url))

    


