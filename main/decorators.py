from django.shortcuts import redirect
from django.http import HttpResponse

# Check the users if they are allowed for the ceratin functionality
def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    print(group)
                    return HttpResponse(f"You belong to {group}")
        return wrapper_func
    return decorators