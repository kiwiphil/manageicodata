from django.db import models

# Create your models here.        
class Blockchain(models.Model):
    """Model representing a blockchain."""
    name = models.CharField(max_length=10, null=False, blank=False)
    
    class Meta:
        ordering = ['name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('blockchain-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}'.format(self.name)
        
class Currency(models.Model):
    """Model representing a currency."""
    symbol = models.CharField(max_length=3, null=False, blank=False)
    
    class Meta:
        ordering = ['symbol']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('currency-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}'.format(self.symbol)
        
class CapUnit(models.Model):
    """Model representing a cap unit."""
    unit = models.CharField(max_length=6, null=False, blank=False)
    
    class Meta:
        ordering = ['unit']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('capunit-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}'.format(self.unit)
        
        
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class ICO(models.Model):
    """Model representing an ICO (but not a specific ICO)."""
    symbol = models.CharField(max_length=10)
    name   = models.CharField(max_length=50)
    
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    #summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    #isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    blockchain = models.ManyToManyField(Blockchain, help_text='Select a Blockchain for this ICO')
    
    def display_blockchain(self):
        return ". ".join(blockchain.name for blockchain in self.blockchain.all()[:3])
        
    display_blockchain.short_description = "Blockchain"
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this ICO."""
        return reverse('ico-detail', args=[str(self.id)])
        
import uuid # Required for unique book instances

class ICOInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular ICO')
    ico = models.ForeignKey('ICO', on_delete=models.SET_NULL, null=True) 
    country = models.CharField(max_length=30)
    start_sale_date = models.DateField(null=True, blank=True)
    last_sale_date  = models.DateField(null=True, blank=True)
    available_tokens = models.PositiveIntegerField(null=False, blank=False)
    total_tokens = models.PositiveIntegerField(null=False, blank=False)
    hard_cap = models.PositiveIntegerField(null=False, blank=False)
    soft_cap = models.PositiveIntegerField(null=False, blank=False)
    
    cap_unit = models.ManyToManyField(CapUnit, help_text='Select a CapUnit for this ICO')

    core_investors = models.DecimalField(max_digits=3, decimal_places=2,null=False, blank=False)
    working_capital = models.DecimalField(max_digits=3, decimal_places=2,null=False, blank=False)
    cost_of_sales = models.DecimalField(max_digits=3, decimal_places=2,null=False, blank=False)
    externals = models.DecimalField(max_digits=3, decimal_places=2,null=False, blank=False)
    public = models.DecimalField(max_digits=3, decimal_places=2,null=False, blank=False)
    number_of_rounds = models.PositiveIntegerField(null=False, blank=False)
    
    highest_mentioned_price = models.DecimalField(max_digits=5, decimal_places=2,null=False, blank=False)
    lowest_mentioned_price = models.DecimalField(max_digits=5, decimal_places=2,null=False, blank=False)
    price_currency = models.ManyToManyField(Currency, help_text='Select a Currency for this ICO')
    
    class Meta:
        ordering = ['ico']

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.ico.symbol)
        

        
        
        
        
        
        
        
        
