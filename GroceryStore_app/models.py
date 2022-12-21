from django.db import models

# Create your models here.


gender_choices = (
    ('m', 'male'),
    ('f', 'female'),
    ('o', 'other'),
)

class Master(models.Model):
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateModified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'master'

    def __str__(self) -> str:
        return self.Email


class UserProfile(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Contact = models.CharField(max_length=50)
    ProfileImage = models.ImageField(upload_to="profiles/", default='avatar.png')
    Gender = models.CharField(max_length=10, choices=gender_choices)
    BirthDate = models.DateField(default="1990-01-01")
    State = models.CharField(max_length=30, blank=True, default='')
    City =  models.CharField(max_length=30, blank=True, default='')
    Address = models.CharField(max_length=30, blank=True, default='')
    Pincode = models.CharField(max_length=6,blank=True,default='')

    class Meta:
        db_table = 'userprofile' 


    def __str__(self) -> str:
        return self.Master.Email

    
class ProductCategory(models.Model):
    Category = models.CharField(max_length=50)

    class Meta:
        db_table = "productcategory"

    def __str__(self) -> str:
        return self.Category


class Product(models.Model):
    Category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    ProductName = models.CharField(max_length=50)
    ProductPrice = models.DecimalField(max_digits=7, decimal_places=2)
    ProductQuantity = models.IntegerField()
    ProductDescription = models.TextField(max_length=250)
    ProductImage = models.ImageField(upload_to="Products/", height_field=None, width_field=None, max_length=None)

    class Meta:
        db_table = "product"

    def __str__(self) -> str:
        return self.ProductName


class Wishlist(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlist'


class Cart(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    TotalPrice = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        db_table = 'cart'

    def __str__(self) -> str:
        return self.Product