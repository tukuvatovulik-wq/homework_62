from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

MANAGER = 'Project Manager'
LEAD = 'Team Lead'
DEVELOPER = 'Developer'


def is_member(user, project):
    return project.members.filter(pk=user.pk).exists()


def can_manage_project(user, project):
    return user.groups.filter(name=MANAGER).exists() and project.owner_id == user.pk


def can_manage_members(user, project):
    return can_manage_project(user, project) or (user.groups.filter(name=LEAD).exists() and is_member(user, project))


def can_create_task(user, project):
    return is_member(user, project) and user.groups.filter(name__in=[MANAGER, LEAD, DEVELOPER]).exists()


def can_delete_task(user, project):
    return can_manage_project(user, project) or (user.groups.filter(name=LEAD).exists() and is_member(user, project))


class ProjectOwnerRoleMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return can_manage_project(self.request.user, self.get_object())


class ProjectTaskRoleMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        task = self.get_object()
        return can_create_task(self.request.user, task.project)


class ProjectTaskDeleteRoleMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        task = self.get_object()
        return can_delete_task(self.request.user, task.project)
