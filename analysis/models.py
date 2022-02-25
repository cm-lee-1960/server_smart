from django.db import models

# Create your models here.
class Register(models.Model):
    category = models.CharField(max_length=10, null=True, blank=True)
    dong = models.IntegerField(null=True, default=0)
    dagyo = models.IntegerField(null=True, default=0)
    coverage = models.IntegerField(null=True, default=0)
    bigct = models.IntegerField(null=True, default=0)
    smallct = models.IntegerField(null=True, default=0)
    inbuiling = models.IntegerField(null=True, default=0)
    nong = models.IntegerField(null=True, default=0)
    theme = models.IntegerField(null=True, default=0)
    sangyong = models.IntegerField(null=True, default=0)
    gaebang = models.IntegerField(null=True, default=0)
    mountain = models.IntegerField(null=True, default=0)
    ship = models.IntegerField(null=True, default=0)
    yooin = models.IntegerField(null=True, default=0)
    searoad = models.IntegerField(null=True, default=0)
    total = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name
