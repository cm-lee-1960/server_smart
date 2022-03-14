from django.utils import timezone
from django.db import models

# Create your models here.
# 측정계획 (MeasPlan)
# 년도, 지역, 네트워크유형, 모폴로지(레벨0, 레벨1, 레벨2)
# year, area, networkId, morph_level0, morph_level1, morph_level2, meas_count 
# create("SELECT .....")
<<<<<<< HEAD
=======
class MeasPlan(models.Model):
   
    networkId_CHOICES = {
        ("5G", "5G"),
        ("LTE", "LTE"),
        ("WiFi", "WiFi+"),
        ("품질취약지역", "품질취약지역"),
    }
    
    area_CHOICES = {
        ("행정동","행정동"),
        ("다중이용시설/교통인프라","다중이용시설/교통인프라"),
        ("커버리지","커버리지"),
        ("상용","상용"),
        ("개방","개방"),
        ("등산로","등산로"),
        ("여객항로","여객항로"),
        ("유인도서","유인도서"),
        ("해안도로","해안도로"),
    }

    molph_CHOICES = {
        ("대도시","대도시"),
        ("중소도시","중소도시"),
        ("농어촌","농어촌"),
        ("인빌딩","인빌딩"),
        ("테마","테마"),
    }

    year = models.IntegerField(null=True, default=0)
    networkId = models.CharField(max_length=30, null=True, blank=True, choices=networkId_CHOICES)
    area = models.CharField(max_length=30, null=True, blank=True, choices=area_CHOICES)
    molph_level0 = models.CharField(max_length=30, null=True, blank=True, choices=molph_CHOICES)
    meas_count = models.IntegerField(null=True, default=0)







>>>>>>> 0f277551f46bb7d33cd5d5a5e6c3cfaf6273b726
class Register(models.Model):
    category = models.CharField(max_length=10, null=True, blank=True)
    dong = models.IntegerField(null=True, default=0)
    dagyo = models.IntegerField(null=True, default=0)
    coverage5g = models.IntegerField(null=True, default=0)
    bigct = models.IntegerField(null=True, default=0)
    smallct = models.IntegerField(null=True, default=0)
    nong = models.IntegerField(null=True, default=0)
    inbuiling = models.IntegerField(null=True, default=0)
    theme = models.IntegerField(null=True, default=0)
    coveragelte = models.IntegerField(null=True, default=0)
    sangyong = models.IntegerField(null=True, default=0)
    gaebang = models.IntegerField(null=True, default=0)
    mountain = models.IntegerField(null=True, default=0)
    ship = models.IntegerField(null=True, default=0)
    yooin = models.IntegerField(null=True, default=0)
    searoad = models.IntegerField(null=True, default=0)
    total = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name






class TodayRegister(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    category = models.CharField(max_length=10, null=True, blank=True)
    jiyok = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField(default=timezone.now, blank = True)
    dongdaco = models.CharField(max_length=30, null=True, blank=True)
    bigsmallnongintheme = models.CharField(max_length=10, null=True, blank=True)
    sanggae =  models.CharField(max_length=10, null=True, blank=True)
    weakjiyok =  models.CharField(max_length=10, null=True, blank=True)
    total = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-date']