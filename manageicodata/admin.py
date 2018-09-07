from django.contrib import admin

# Register your models here.
from .models import Blockchain, CapUnit, Currency, ICO, ICOInstance, Country

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django import forms
from django.conf.urls import url
from django.urls import include, path

import pycountry
import csv
from django.utils import timezone
from django.shortcuts import render, redirect

from io import TextIOWrapper


#admin.site.register(Blockchain)
admin.site.register(CapUnit)
admin.site.register(Currency)
#admin.site.register(ICO)
#admin.site.register(ICOInstance)

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


# Define the admin class
class BlockchainAdmin(admin.ModelAdmin):
    list_display = ['blockchain_name']
    pass

# Register the admin class with the associated model
admin.site.register(Blockchain, BlockchainAdmin)

# Register the Admin classes for Country using the decorator
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    actions = ['load_countries']
    list_display = ['country_name']
    change_list_template = 'admin/manageicodata/country/change_list.html'
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('populate/', self.populate),
        ]
        return my_urls + urls

    def populate(self, request):
        number_countries_in_table = Country.objects.count()
        if number_countries_in_table > 0: Country.objects.all().delete()
           
        allc = [c.name for c in pycountry.countries]
        country_list = []
        for c in allc:
            tmp = Country(country_name=c)
            country_list.append(tmp)
        Country.objects.bulk_create(country_list)
        self.message_user(request, "Country Table has been successfully populated.")
        return HttpResponseRedirect("../") #Redirect

    def load_countries(self, request, queryset):
        return 
    load_countries.short_description = "Populate Countries Table."
    
    pass

#
class ICOForm(forms.ModelForm):
    class Meta:
        model = ICO
        fields = '__all__'
        
    def save(self, commit=True):
        instance = super(ICOForm, self).save(commit=False)
        instance.last_user = self.request.user.username
        instance.last_update = timezone.now()
        if commit: instance.save()
        return instance

# Register the Admin classes for ICO using the decorator
@admin.register(ICO)
class ICOAdmin(admin.ModelAdmin):
    form = ICOForm
    list_display = ['symbol', 'name', 'last_user', 'last_update'] #'display_blockchain']
    change_list_template = "admin/manageicodata/ico/change_list.html"
    list_filter = ['symbol', 'name']
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls
        
    # This is important to have because this provides the
    # "request" object to "clean" method
    def get_form(self, request, obj=None, **kwargs):
        form = super(ICOAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form
        
    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_file = TextIOWrapper(csv_file)
            reader = csv.reader(csv_file)
            #skip header
            next(reader)
            # Create ICO objects from passed in data
            for row in reader:
                if row[0]=="": continue
                _, created = ICO.objects.get_or_create(
                     symbol      = row[0],
                     name        = row[1],
                     last_user   = request.user.username,
                     last_update = timezone.now(),
                     )
            self.message_user(request, "Your CSV file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/manageicodata/ico/csv_form.html", payload)
    
    pass

#
class ICOInstanceForm(forms.ModelForm):
    class Meta:
        model = ICOInstance
        fields = '__all__'

    def clean(self):
        start_date = self.cleaned_data.get('start_sale_date')
        end_date = self.cleaned_data.get('last_sale_date')
        if start_date > end_date:
           raise forms.ValidationError("Dates are incorrect, start_sale_date after last_sale_date")
        # 'core_investors', 'working_capital', 'cost_of_sales', 'externals', 'public'
        core_i = self.cleaned_data.get('core_investors')
        work_c = self.cleaned_data.get('working_capital')
        cost_o = self.cleaned_data.get('cost_of_sales')
        exte_r = self.cleaned_data.get('externals')
        publ_i = self.cleaned_data.get('public')
        sum_token_dist = core_i + work_c + cost_o + exte_r + publ_i
        if sum_token_dist != 1.0:
           errmsg = "Token Distribution must sum to 1.0, currently totals {0}.".format(sum_token_dist) 
           raise forms.ValidationError(errmsg)
           
        return self.cleaned_data
        
    def save(self, commit=True):
        instance = super(ICOInstanceForm, self).save(commit=False)
        instance.last_user = self.request.user.username
        instance.last_update = timezone.now()
        if commit: instance.save()
        return instance
        


        
# Register the Admin classes for ICOInstance using the decorator
@admin.register(ICOInstance) 
class ICOInstanceAdmin(admin.ModelAdmin):
    form = ICOInstanceForm 
    actions = ['export_csv']
    list_display = ['ico', 'display_blockchain', 'last_user', 'last_update', 
                    'start_sale_date',
                    'last_sale_date']
    list_filter = ['country', 'blockchain_name', 'hard_cap_unit', 'soft_cap_unit', 
                   'number_of_rounds',
                   'start_sale_date', 'last_sale_date', 'price_currency'] 
    fieldsets = (
        (None, {
            'fields': ('ico', 'blockchain_name', 'country') 
            }),
            ('Token Numbers', {
            'fields': (('available_tokens', 'total_tokens', 'total_tokens_not_mentioned',
                        'total_tokens_unlimited'), 
                       ('hard_cap', 'soft_cap'), ('hard_cap_unit', 'soft_cap_unit'))
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
            ('Comments', {
            'fields': ('comments',)
            }),
    ) 
    
    def display_blockchain(self, obj):
        return ". ".join([p.blockchain_name for p in obj.blockchain_name.all()[:3]]) 
    display_blockchain.short_description = "Blockchain"
    
    # This is important to have because this provides the
    # "request" object to "clean" method
    def get_form(self, request, obj=None, **kwargs):
        form = super(ICOInstanceAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form
    
    def export_csv(self, request, queryset):
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=ico_instances.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) 
        # write column headings
        writer.writerow([
                smart_str(u"ico"),
                smart_str(u"last_user"),
                smart_str(u"last_update"),
                smart_str(u"blockchain_name"),
                smart_str(u"country"),
                smart_str(u'available_tokens'), 
                smart_str(u'total_tokens'), 
                smart_str(u'total_tokens_not_mentioned'),
                smart_str(u'total_tokens_unlimited'),
                smart_str(u'hard_cap'), 
                smart_str(u'soft_cap'),
                smart_str(u'hard_cap_unit'), 
                smart_str(u'soft_cap_unit'),
                smart_str(u'core_investors'),
                smart_str(u'working_capital'), 
                smart_str(u'cost_of_sales'),
                smart_str(u'externals'), 
                smart_str(u'public'),
                smart_str(u'number_of_rounds'),
                smart_str(u'start_sale_date'), 
                smart_str(u'last_sale_date'),
                smart_str(u'highest_mentioned_price'), 
                smart_str(u'lowest_mentioned_price'),
                smart_str(u'price_currency'),
                smart_str(u'comments'),
        ])
        # write row contents
        num_rows = len(queryset)
        for obj in queryset:
            writer.writerow([
                smart_str(obj.ico),
                smart_str(obj.last_user),
                smart_str(obj.last_update),
                smart_str(". ".join([p.blockchain_name for p in obj.blockchain_name.all()[:3]])),
                smart_str(obj.country),
                smart_str(obj.available_tokens), 
                smart_str(obj.total_tokens), 
                smart_str(obj.total_tokens_not_mentioned),
                smart_str(obj.total_tokens_unlimited),
                smart_str(obj.hard_cap), 
                smart_str(obj.soft_cap), 
                smart_str(". ".join([p.unit for p in obj.hard_cap_unit.all()[:3]])),
                smart_str(". ".join([p.unit for p in obj.soft_cap_unit.all()[:3]])),
                smart_str(obj.core_investors),
                smart_str(obj.working_capital), 
                smart_str(obj.cost_of_sales),
                smart_str(obj.externals), 
                smart_str(obj.public),
                smart_str(obj.number_of_rounds),
                smart_str(obj.start_sale_date), 
                smart_str(obj.last_sale_date),
                smart_str(obj.highest_mentioned_price), 
                smart_str(obj.lowest_mentioned_price),
                smart_str(". ".join([p.symbol for p in obj.price_currency.all()[:3]])),
                smart_str(obj.comments),
            ])
        msg = "{0} ICO Instances written to CSV.".format(num_rows)
        messages.add_message(request, messages.INFO, msg)    
        return response    
    export_csv.short_description = "Export ICO Instances to CSV."






