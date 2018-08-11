from django.shortcuts import render

# Create your views here.
from .models import ICO, ICOInstance, Blockchain, CapUnit, Currency

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_icos = ICO.objects.all().count()
    num_instances = ICOInstance.objects.all().count()
    
    # Available books (status = 'a')
    #num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_blockchains = Blockchain.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_icos': num_icos,
        'num_instances': num_instances,
        'num_blockchains': num_blockchains,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
    
from django.views import generic

class ICOListView(generic.ListView):
    model = ICO
    paginate_by = 10
    
class ICODetailView(generic.DetailView):
    model = ICO
    
    
    
    
    
    
    
