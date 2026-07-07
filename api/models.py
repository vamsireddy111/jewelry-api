from django.db import models

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()

    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    price = models.FloatField()
    discount = models.FloatField(default=0)

    base_metal = models.CharField(max_length=50)
    polish = models.CharField(max_length=50)

    rating = models.FloatField(default=0)

    image_url = models.URLField()

    def __str__(self):
        return self.name