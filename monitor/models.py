from django.db import models

# Create your models here.
class Phone(models.Model):
    phone_no = models.BigIntegerField()
    avg_downloadTransfer = models.FloatField()
    avg_uploadTransfer =models.FloatField()
    status = models.CharField(max_length=10)
    total_count = models.IntegerField()
    
    def add_measure_data(mdata):
        pass
        
class Measuredata(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    neworkid = models.CharField(max_length=10)
    meastime = models.BigIntegerField()
    downloadTransfer =models.IntegerField()
    uploadTransfer = models.IntegerField()

    def __str__(self):
         return self.phone

class Message(models.Model):
    pass

#메세지가 저장될때 저장후 Send_message 호출 구현
