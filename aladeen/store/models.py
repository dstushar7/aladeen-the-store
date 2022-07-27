from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # products

class Collection(models.Model):
    title = models.CharField(max_length=255)
    # Circular Dependency
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

# Creating Product entities
class Product(models.Model):
    title = models.CharField(max_length=255) # go to django fieldtypes to select the appropriate fieldtype and fill required parameters
    # varchar(255) type column
    slug = models.SlugField()
    description = models.TextField() # Bigger data type
    unit_price = models.DecimalField(max_digits=6,decimal_places=2) # not max length but counting digits 9999.99 is the highest price here
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # many to many field
    promotions = models.ManyToManyField(Promotion, related_name='products') # related_name will create a attribute in the promotion class

# Creating Customer entities
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    # Now we will create an attribute that will take only 3 values as input, mainly creating a choice field from dropdown menu
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)


# Creating Order entities
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS = [
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_COMPLETE,'Complete'),
        (PAYMENT_STATUS_FAILED,'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


# Creating 1 to 1 relationships
# class Address(models.Model):
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     customer = models.OneToOneField(Customer, on_delete=models.CASCADE , primary_key=True) 
    # Defining the one to one relation with customer

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


# Creating 1 to many relationships
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.PositiveIntegerField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # Defining the one to one relation with customer

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()