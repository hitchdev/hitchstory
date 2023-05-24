from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return redirect('/todos')
