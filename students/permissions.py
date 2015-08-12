from permissions.utils import register_permission
from permissions.utils import register_role
from permissions.utils import grant_permission
from permissions.utils import has_permission

from .models import Student

view = register_permission("View", "view")
edit = register_permission("Edit", "edit")
delete = register_permission("Delete", "delete")
add = register_permission("Add", "add")
manage_content = register_permission("Manage content", "manage_content")

school_admin = register_role("Admin")
educator = register_role("Educator")
guardian = register_role("Guardian")
student = register_role("Student")

#school_admin permissions
grant_permission(Student, school_admin, "view")
grant_permission(Student, school_admin, "delete")

#educator permissions
grant_permission(Student, educator, "view")
grant_permission(Student, educator, "edit")
grant_permission(Student, educator, "add")

#student permissions
grant_permission(Student.avatar, student, "edit")
grant_permission(Student, student, "view")
# grant_permission(Spend_points, student, "add")




def has_perm(self, user_obj, perm, obj=None):
    return has_permission(obj, user_obj, perm)