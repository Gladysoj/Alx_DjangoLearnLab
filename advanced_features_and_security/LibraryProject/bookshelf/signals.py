# bookshelf/signals.py
from django.contrib.auth.models import Group, Permission

def create_groups(sender, **kwargs):
    can_view = Permission.objects.get(codename="can_view")
    can_create = Permission.objects.get(codename="can_create")
    can_edit = Permission.objects.get(codename="can_edit")
    can_delete = Permission.objects.get(codename="can_delete")

    editors, _ = Group.objects.get_or_create(name="Editors")
    viewers, _ = Group.objects.get_or_create(name="Viewers")
    admins, _ = Group.objects.get_or_create(name="Admins")

    editors.permissions.set([can_edit, can_create])
    viewers.permissions.set([can_view])
    admins.permissions.set([can_view, can_create, can_edit, can_delete])
