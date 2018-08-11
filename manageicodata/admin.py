from django.contrib import admin

# Register your models here.
from .models import Blockchain, CapUnit, Currency, ICO, ICOInstance

#admin.site.register(Blockchain)
admin.site.register(CapUnit)
admin.site.register(Currency)
#admin.site.register(ICO)
#admin.site.register(ICOInstance)

# Define the admin class
class BlockchainAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

# Register the admin class with the associated model
admin.site.register(Blockchain, BlockchainAdmin)

# Register the Admin classes for ICO using the decorator
@admin.register(ICO)
class ICOAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'display_blockchain']
    pass

# Register the Admin classes for ICOInstance using the decorator
@admin.register(ICOInstance) 
class ICOInstanceAdmin(admin.ModelAdmin):
    list_filter = ['country', 'cap_unit', 'number_of_rounds',
                   'start_sale_date', 'last_sale_date', 'price_currency'] 
    
    fieldsets = (
        (None, {
            'fields': ('id', 'ico', 'country')
            }),
            ('Token Numbers', {
            'fields': (('available_tokens', 'total_tokens'), ('hard_cap', 
                       'soft_cap'), 'cap_unit')
            }),
            ('Token Distribution', {
            'fields': ('core_investors', 'working_capital', 'cost_of_sales',
                       'externals', 'public')
            }),
            ('Token Sales', {
            'fields': ('number_of_rounds', ('start_sale_date', 'last_sale_date'))
            }),
            ('Token Pricing', {
            'fields': ('highest_mentioned_price', 'lowest_mentioned_price',
                       'price_currency')
            }),
    ) 
    
    pass
    
    
