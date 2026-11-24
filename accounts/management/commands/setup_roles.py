from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from tasks.models import Project, Task


class Command(BaseCommand):
    help = 'Создаёт роли и демонстрационных пользователей manager, lead, dev.'

    def handle(self, *args, **options):
        project_ct = ContentType.objects.get_for_model(Project)
        task_ct = ContentType.objects.get_for_model(Task)
        roles = {
            'Project Manager': [('add_project', project_ct), ('change_project', project_ct), ('delete_project', project_ct), ('add_task', task_ct), ('change_task', task_ct), ('delete_task', task_ct)],
            'Team Lead': [('add_task', task_ct), ('change_task', task_ct), ('delete_task', task_ct)],
            'Developer': [('add_task', task_ct), ('change_task', task_ct)],
        }
        groups = {}
        for name, permission_pairs in roles.items():
            group, _ = Group.objects.get_or_create(name=name)
            group.permissions.set([Permission.objects.get(codename=code, content_type=ct) for code, ct in permission_pairs])
            groups[name] = group
        for username, group_name in [('manager', 'Project Manager'), ('lead', 'Team Lead'), ('dev', 'Developer')]:
            user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com'})
            if created:
                user.set_password(username)
                user.save()
            user.groups.set([groups[group_name]])
        self.stdout.write(self.style.SUCCESS('Роли и пользователи готовы.'))
