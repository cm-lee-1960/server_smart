from django.utils import timezone
from django.db import models

# Create your models here.
# 측정계획 (MeasPlan)
# 년도, 지역, 네트워크유형, 모폴로지(레벨0, 레벨1, 레벨2)
# year, area, networkId, morph_level0, morph_level1, morph_level2, meas_count 
# create("SELECT .....")
class MeasPlan(models.Model):
   
    networkId_CHOICES = {
        ("5G", "5G"),
        ("LTE", "LTE"),
        ("WiFi", "WiFi+"),
        ("품질취약지역", "품질취약지역"),
    }
    
    area_CHOICES = {
        ("1.행정동","행정동"),
        ("2.다중이용시설/교통인프라","다중이용시설/교통인프라"),
        ("3.커버리지","커버리지"),
        ("4.상용","상용"),
        ("5.개방","개방"),
        ("6.등산로","등산로"),
        ("7.여객항로","여객항로"),
        ("8.유인도서","유인도서"),
        ("9.해안도로","해안도로"),
    }

    molph_CHOICES = {
        ("1.대도시","대도시"),
        ("2.중소도시","중소도시"),
        ("3.농어촌","농어촌"),
        ("4.인빌딩","인빌딩"),
        ("5.테마","테마"),
    }

    year = models.IntegerField(null=True, default=0, verbose_name="대상년도", help_text="대상년도를 입력해주세요.")
    networkId = models.CharField(max_length=30, null=True, blank=True, choices=networkId_CHOICES, verbose_name="네트워크구분", help_text="측정 네트워크를 선택해주세요.")
    area = models.CharField(max_length=30, null=True, blank=True, choices=area_CHOICES, verbose_name="측정위치", help_text="측정위치 구분자 선택해주세요.")
    molph_level0 = models.CharField(max_length=30, null=True, blank=True, choices=molph_CHOICES, verbose_name="측정위치1", help_text="측정위치1 구분자 선택해주세요.")
    meas_count = models.IntegerField(null=True, default=0)

# Create your models here.
# 측정결과 (MeasResult)
# 측정일자, 측정관련정보, 지역, 네트워크유형, 모폴로지(레벨0, 레벨1, 레벨2)
# date, info, area, networkId, morph_level0, morph_level1, morph_level2
# create("SELECT .....")

class MeasResult(models.Model):

    networkId_CHOICES = {
        ("5G", "5G"),
        ("LTE", "LTE"),
        ("WiFi", "WiFi"),
        ("품질취약지역", "품질취약지역"),
        }
    
    area_CHOICES = {
        ("1.행정동","행정동"),
        ("2.다중이용시설/교통인프라","다중이용시설/교통인프라"),
        ("3.커버리지","커버리지"),
        ("4.상용","상용"),
        ("5.개방","개방"),
        ("6.등산로","등산로"),
        ("7.여객항로","여객항로"),
        ("8.유인도서","유인도서"),
        ("9.해안도로","해안도로"),
    }

    molph0_CHOICES = {
        ("1.대도시","대도시"),
        ("2.중소도시","중소도시"),
        ("3.농어촌","농어촌"),
        ("4.인빌딩","인빌딩"),
        ("5.테마","테마"),
    }

    date = models.DateField(default=timezone.now, verbose_name="측정일자", help_text="측정일자를 반드시 입력해야 합니다.")
    info = models.CharField(max_length=30, null=True, blank=True, verbose_name="측정정보", help_text="측정정보를 적어주세요.")
    networkId = models.CharField(max_length=30, null=True, blank=True, choices=networkId_CHOICES, verbose_name="네트워크구분", help_text="측정 네트워크를 선택해주세요.")
    area = models.CharField(max_length=30, null=True, blank=True, choices=area_CHOICES, verbose_name="측정위치", help_text="측정위치 구분자 선택해주세요.")
    molph_level0 = models.CharField(max_length=30, null=True, blank=True, choices=molph0_CHOICES, verbose_name="측정위치1", help_text="측정위치1 구분자 선택해주세요.")
    molph_level1 = models.CharField(max_length=30, null=True, blank=True, verbose_name="지역", help_text="측정지역을 적어주세요.")
    # classify = models.CharField(default = )
    


###############################################################################################################################################################################
#3.16 측정대상 모델(수정완료)(클래스명 변경 필요, MeasPlan으로 변경예정)
###############################################################################################################################################################################
class Register(models.Model):
    planYear = models.IntegerField(null=True, default=0)
    area1 = models.IntegerField(null=True, default=0)
    area2 = models.IntegerField(null=True, default=0)
    area3 = models.IntegerField(null=True, default=0)
    area4 = models.IntegerField(null=True, default=0)
    area5 = models.IntegerField(null=True, default=0)
    area6 = models.IntegerField(null=True, default=0)
    area7 = models.IntegerField(null=True, default=0)
    area8 = models.IntegerField(null=True, default=0)
    area9 = models.IntegerField(null=True, default=0)
    area10 = models.IntegerField(null=True, default=0)
    area11 = models.IntegerField(null=True, default=0)
    area12 = models.IntegerField(null=True, default=0)
    area13 = models.IntegerField(null=True, default=0)
    area14 = models.IntegerField(null=True, default=0)
    area15 = models.IntegerField(null=True, default=0)
    total5G = models.IntegerField(null=True, default=0)
    totalLTE = models.IntegerField(null=True, default=0)
    totalWiFi = models.IntegerField(null=True, default=0)
    totalWeakArea = models.IntegerField(null=True, default=0)
    total = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name

# class Register(models.Model):
#     category = models.CharField(max_length=10, null=True, blank=True)
#     dong = models.IntegerField(null=True, default=0)
#     dagyo = models.IntegerField(null=True, default=0)
#     coverage5g = models.IntegerField(null=True, default=0)
#     bigct = models.IntegerField(null=True, default=0)
#     smallct = models.IntegerField(null=True, default=0)
#     nong = models.IntegerField(null=True, default=0)
#     inbuiling = models.IntegerField(null=True, default=0)
#     theme = models.IntegerField(null=True, default=0)
#     coveragelte = models.IntegerField(null=True, default=0)
#     sangyong = models.IntegerField(null=True, default=0)
#     gaebang = models.IntegerField(null=True, default=0)
#     mountain = models.IntegerField(null=True, default=0)
#     ship = models.IntegerField(null=True, default=0)
#     yooin = models.IntegerField(null=True, default=0)
#     searoad = models.IntegerField(null=True, default=0)
#     total = models.IntegerField(null=True, default=0)
#     def __str__(self):
#         return self.name


###############################################################################################################################################################################
#3.16 측정완료대상 모델(수정중)(클래스명 변경 필요, MeasResult로 변경예정)
#3.17 수정완료(클래스명 변경 필요, MeasResult로 변경예정)
###############################################################################################################################################################################

# class TodayRegister(models.Model):
#     name = models.CharField(max_length=30, null=True, blank=True)
#     category = models.CharField(max_length=10, null=True, blank=True)
#     jiyok = models.CharField(max_length=10, null=True, blank=True)
#     date = models.DateField(default=timezone.now, blank = True)
#     dongdaco = models.CharField(max_length=30, null=True, blank=True)
#     bigsmallnongintheme = models.CharField(max_length=10, null=True, blank=True)
#     sanggae =  models.CharField(max_length=10, null=True, blank=True)
#     weakjiyok =  models.CharField(max_length=10, null=True, blank=True)
#     total = models.IntegerField(null=True, default=0)
#     def __str__(self):
#         return self.name
#     class Meta:
#         ordering = ['-date']


class TodayRegister(models.Model):
    date = models.DateField(default=timezone.now, blank = True)
    measinfo = models.CharField(max_length=30, null=True, blank=True)
    networkId = models.CharField(max_length=30, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    area = models.CharField(max_length=30, null=True, blank=True)
    molph_level0 = models.CharField(max_length=30, null=True, blank=True)
    molph_level1 = models.CharField(max_length=30, null=True, blank=True)
   
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-date']



###############################################################################################################################################################################
#3.17 일일보고 추가 메세지 등록모델(수정중)
###############################################################################################################################################################################

class ReportMessage(models.Model):
    msg1 = models.CharField(max_length=50, null=True, blank=True)
    msg2 = models.CharField(max_length=50, null=True, blank=True)
    msg3 = models.CharField(max_length=50, null=True, blank=True)
    msg4 = models.CharField(max_length=50, null=True, blank=True)
    msg5 = models.CharField(max_length=50, null=True, blank=True)
    msg6 = models.CharField(max_length=50, null=True, blank=True)


###############################################################################################################################################################################
#3.17 일일보고 작년 측정 결과 등록 모델 5G(수정중)
###############################################################################################################################################################################

class MeasLastyear5G(models.Model):
    area1DL = models.FloatField(null=True, default=0)
    area1UL = models.FloatField(null=True, default=0)
    area1LTE = models.FloatField(null=True, default=0)
    area1succ = models.FloatField(null=True, default=0)
    area1delay = models.FloatField(null=True, default=0)

    area2DL = models.FloatField(null=True, default=0)
    area2UL = models.FloatField(null=True, default=0)
    area2LTE = models.FloatField(null=True, default=0)
    area2succ = models.FloatField(null=True, default=0)
    area2delay = models.FloatField(null=True, default=0)

    area3DL = models.FloatField(null=True, default=0)
    area3UL = models.FloatField(null=True, default=0)
    area3LTE = models.FloatField(null=True, default=0)
    area3succ = models.FloatField(null=True, default=0)
    area3delay = models.FloatField(null=True, default=0)

    area4DL = models.FloatField(null=True, default=0)
    area4UL = models.FloatField(null=True, default=0)
    area4LTE = models.FloatField(null=True, default=0)
    area4succ = models.FloatField(null=True, default=0)
    area4delay = models.FloatField(null=True, default=0)

    area5DL = models.FloatField(null=True, default=0)
    area5UL = models.FloatField(null=True, default=0)
    area5LTE = models.FloatField(null=True, default=0)
    area5succ = models.FloatField(null=True, default=0)
    area5delay = models.FloatField(null=True, default=0)

    area6DL = models.FloatField(null=True, default=0)
    area6UL = models.FloatField(null=True, default=0)
    area6LTE = models.FloatField(null=True, default=0)
    area6succ = models.FloatField(null=True, default=0)
    area6delay = models.FloatField(null=True, default=0)

    area7DL = models.FloatField(null=True, default=0)
    area7UL = models.FloatField(null=True, default=0)
    area7LTE = models.FloatField(null=True, default=0)
    area7succ = models.FloatField(null=True, default=0)
    area7delay = models.FloatField(null=True, default=0)

    areatotalDL = models.FloatField(null=True, default=0)
    areatotalUL = models.FloatField(null=True, default=0)
    areatotalLTE = models.FloatField(null=True, default=0)
    areatotalsucc = models.FloatField(null=True, default=0)
    areatotaldelay = models.FloatField(null=True, default=0)


###############################################################################################################################################################################
#3.17 일일보고 작년 측정 결과 등록 모델 LTE(수정중)
###############################################################################################################################################################################

class MeasLastyearLTE(models.Model):
    area1DL = models.FloatField(null=True, default=0)
    area1UL = models.FloatField(null=True, default=0)
   
    area1succ = models.FloatField(null=True, default=0)
    area1delay = models.FloatField(null=True, default=0)

    area2DL = models.FloatField(null=True, default=0)
    area2UL = models.FloatField(null=True, default=0)
    
    area2succ = models.FloatField(null=True, default=0)
    area2delay = models.FloatField(null=True, default=0)

    area3DL = models.FloatField(null=True, default=0)
    area3UL = models.FloatField(null=True, default=0)
    
    area3succ = models.FloatField(null=True, default=0)
    area3delay = models.FloatField(null=True, default=0)

    area4DL = models.FloatField(null=True, default=0)
    area4UL = models.FloatField(null=True, default=0)
    
    area4succ = models.FloatField(null=True, default=0)
    area4delay = models.FloatField(null=True, default=0)

    area5DL = models.FloatField(null=True, default=0)
    area5UL = models.FloatField(null=True, default=0)
    
    area5succ = models.FloatField(null=True, default=0)
    area5delay = models.FloatField(null=True, default=0)

    area6DL = models.FloatField(null=True, default=0)
    area6UL = models.FloatField(null=True, default=0)
    
    area6succ = models.FloatField(null=True, default=0)
    area6delay = models.FloatField(null=True, default=0)

    areatotalDL = models.FloatField(null=True, default=0)
    areatotalUL = models.FloatField(null=True, default=0)
    
    areatotalsucc = models.FloatField(null=True, default=0)
    areatotaldelay = models.FloatField(null=True, default=0)
