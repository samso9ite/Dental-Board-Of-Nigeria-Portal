from schPortal.models import School

def index_access_control(request):
    if request.user.is_authenticated:
        try:
            index_access= School.objects.get(User=request.user.id)
        except School.DoesNotExist:
            index_access = None
    else: 
        index_access = None
    return{
        'index_access': index_access
    }