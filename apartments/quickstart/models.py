from django.db import models

# Create your models here.

class Category(models.Model):
    typeOfAd = models.CharField(max_length=250)
    # active = models.BooleanField(default=True)

    def __str__(self):
        return self.typeOfAd

    class Meta:
        verbose_name_plural = "Categories"

class Advertisement(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media/images', blank=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=10, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, blank=True)
    year = models.DateTimeField()
    area = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title