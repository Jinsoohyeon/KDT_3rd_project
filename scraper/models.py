from django.db import models

# Create your models here.
class Location(models.Model):
    location_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, null=True)
    ope_time = models.CharField(max_length=100, null=True)
    rec_time = models.CharField(max_length=50, null=True)
    addrs = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f'{self.pk}=={self.location_name}'

class TouristReview(models.Model):
    location_name = models.CharField(max_length=100)
    rate = models.CharField(max_length=5, null=True)
    year = models.CharField(max_length=5, null=True)
    month = models.CharField(max_length=5, null=True)
    day = models.CharField(max_length=4, null=True)
    review = models.CharField(max_length=10000, null=True)

    def __str__(self):
        return f'{self.pk}=={self.location_name}=={self.review[0:20]}'


# class TripadvisorReview(models.Model):
#     location_name = models.CharField(max_length=100)
#     rate = models.CharField(max_length=5)
#     date = models.CharField(max_length=10)
#     member = models.CharField(max_length=20, null=True)
#     review = models.CharField(max_length=10000, null=True)

#     def __str__(self):
#         return f'{self.pk}=={self.location_name}=={self.review[0:20]}'

# class TripdotComReview(models.Model):
#     location_name = models.CharField(max_length=100)
#     rate = models.CharField(max_length=5)
#     date = models.CharField(max_length=10)
#     review = models.CharField(max_length=10000, null=True)

#     def __str__(self):
#         return f'{self.pk}=={self.location_name}=={self.review[0:20]}'