from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    # fields = ['title','slug']
    prepopulated_fields = {
        'slug':['title']
    }
    list_display = ['title','unit_price', 'inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection','last_update',InventoryFilter]
    search_fields = ['product']


    def collection_title(self,product):
        return product.collection.title


    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were succesfully updated',
            messages.ERROR
        )


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    max_num = 10
    min_num = 1
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id','placed_at','customer']
    autocomplete_fields = ['customer']



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith','last_name__startswith']

    @admin.display(ordering='orders_count')
    def orders_count(self,customer):
        # return customer.orders_count
        url = (
            reverse('admin:store_order_changelist') 
            + '?' 
            + urlencode({
                'customer__id':customer.id
        }))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count = Count('order')
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title__istartswith']

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        # We can add html format codes in here
        # return format_html('<a href="https://www.google.com">{}</a>',collection.products_count)
        # url = reverse('admin:app_model_page') # Format
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id' : str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
        
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )