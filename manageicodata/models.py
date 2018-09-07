from django.db import models

# Create your models here.        
class Blockchain(models.Model):
    """Model representing a blockchain."""
    blockchain_name = models.CharField(primary_key=True, max_length=10, null=False, blank=False)
    
    class Meta:
        ordering = ['blockchain_name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('blockchain-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}'.format(self.blockchain_name)
        
class Currency(models.Model):
    """Model representing a currency."""
    symbol = models.CharField(primary_key=True, max_length=3, null=False, blank=False)
    
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
    unit = models.CharField(primary_key=True, max_length=6, null=False, blank=False)
    
    class Meta:
        ordering = ['unit']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('capunit-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}'.format(self.unit)
        
        
class Country(models.Model):
    """Model representing a Country."""
    country_name = models.CharField(primary_key=True, max_length=100, null=False, blank=False)
    
    class Meta:
        ordering = ['country_name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular country instance."""
        return reverse('country-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}'.format(self.country_name)
        
        
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances


class ICO(models.Model):
    """Model representing an ICO (but not a specific ICO)."""
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4,
    #                      help_text='Unique ID for this particular ICO')
    symbol = models.CharField(max_length=15, null=True)
    name   = models.CharField(max_length=50, null=True)
    last_user = models.CharField(max_length=50, null=False, blank=True, default="")
    last_update = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together=(("symbol", "name"),)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this ICO."""
        return reverse('ico-detail', args=[str(self.id)])
        


class ICOInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular ICO')
    ico = models.ForeignKey('ICO', on_delete=models.CASCADE, null=True) 
    
    blockchain_name = models.ManyToManyField(Blockchain, 
                                       help_text='Select a Blockchain for this ICO')
    
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True,
                                       help_text='Select a Country for this ICO')
    start_sale_date = models.DateField(null=True, blank=True,
                                       help_text='The date when ICO tokens first start to sell.')
    last_sale_date  = models.DateField(null=True, blank=True,
                                       help_text='The last date when ICO tokens will be sold.')
    available_tokens = models.DecimalField(max_digits=14, decimal_places=0, null=False, blank=False,
                                       help_text='The number of tokens available for sale to the public.')
    total_tokens = models.DecimalField(max_digits=14, decimal_places=0, null=False, blank=False,
                                       help_text='The total number of tokens in this ICO')
    total_tokens_not_mentioned = models.BooleanField(default=False,
                                       help_text='Check if Total Tokens not mentioned.')
    total_tokens_unlimited = models.BooleanField(default=False,
                                       help_text='Check if Total Tokens are unlimited.') 
    hard_cap = models.DecimalField(max_digits=14, decimal_places=0, null=False, blank=False,
                                       help_text='The maximum number of tokens to be sold for this ICO.')                               
    hard_cap_unit = models.ManyToManyField(CapUnit, 
                                       related_name='%(class)s_hardcap',
                                       help_text='Select a CapUnit for this ICO')
    soft_cap = models.DecimalField(max_digits=14, decimal_places=0, null=False, blank=False,
                                       help_text='The minimum number of tokens to be sold if ICO will go ahead.')
    soft_cap_unit = models.ManyToManyField(CapUnit, 
                                       related_name='%(class)s_softcap',   
                                       help_text='Select a CapUnit for this ICO')

    core_investors = models.DecimalField(max_digits=5, decimal_places=4,null=False, blank=False,
                                       help_text='something informative.')
    working_capital = models.DecimalField(max_digits=5, decimal_places=4,null=False, blank=False,
                                       help_text='something informative.')
    cost_of_sales = models.DecimalField(max_digits=5, decimal_places=4,null=False, blank=False,
                                       help_text='something informative.')
    externals = models.DecimalField(max_digits=5, decimal_places=4,null=False, blank=False,
                                       help_text='something informative.')
    public = models.DecimalField(max_digits=5, decimal_places=4,null=False, blank=False,
                                       help_text='something informative.')
    number_of_rounds = models.PositiveIntegerField(null=False, blank=False,
                                       help_text='The number of rounds in the ICO Token Sale.')
    
    highest_mentioned_price = models.DecimalField(max_digits=12, decimal_places=6,null=False, blank=False,
                                       help_text='Highest price a token sold for during ICO.')
    lowest_mentioned_price = models.DecimalField(max_digits=12, decimal_places=6,null=False, blank=False,
                                       help_text='Lowest price a token sold for during ICO.')
    price_currency = models.ManyToManyField(Currency, 
                                       help_text='The currency used to buy this ICOs tokens.')
    
    comments = models.TextField(max_length=400, null=False, blank=True, default="",
                                       help_text='Report any anomalies and/or ask questions.')
                                       
    last_user = models.CharField(max_length=50, null=False, blank=True, default="")
    last_update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ico']
        
    def __str__(self):
        """String for representing the Model object."""
        return str(self.ico)
        
        

        
        
        
        
        
        
        
        
