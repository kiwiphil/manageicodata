from django.contrib import admin

# Register your models here.
from .models import Blockchain, CapUnit, Currency, ICO, ICOInstance

from django.http import HttpResponse
from django.contrib import messages

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

#
      
        
# Register the Admin classes for ICOInstance using the decorator
@admin.register(ICOInstance) 
class ICOInstanceAdmin(admin.ModelAdmin):
    actions = ['export_csv']
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
    
    def export_csv(self, request, queryset):
        import csv
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=ico_instances.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) 
        # write column headings
        writer.writerow([
                smart_str(u"id"),
                smart_str(u"ico"),
                smart_str(u"country"),
        ])
        # write row contents
        num_rows = len(queryset)
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.ico),
                smart_str(obj.country),
            ])
        msg = "{0} ICO Instances written to CSV.".format(num_rows)
        messages.add_message(request, messages.INFO, msg)    
        #self.message_user(request, "{0} ICO Instances written to CSV.".format(num_rows))
        return response    
    export_csv.short_description = "Export ICO Instances to CSV."






