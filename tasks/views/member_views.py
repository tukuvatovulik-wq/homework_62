from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from tasks.models import Project
from tasks.permissions import can_manage_members

@login_required
def project_members(request, pk):
    project = get_object_or_404(Project, pk=pk)
    allowed = can_manage_members(request.user, project)
    if not allowed:
        return redirect('tasks:project_detail', pk=pk)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        member = get_object_or_404(User, pk=user_id)
        if action == 'add':
            project.members.add(member)
        elif action == 'remove' and member != project.owner:
            project.members.remove(member)
        return redirect('tasks:project_members', pk=pk)
    return render(request, 'projects/project_members.html', {'project': project, 'users': User.objects.exclude(pk__in=project.members.values_list('pk', flat=True))})
