from django.db import models
from django.conf import settings
from management.models import Center

########################################################################################################################
# 프로파일 정보
# ----------------------------------------------------------------------------------------------------------------------
# 2022.05.10 - 사용자 계정에 소속 운용센터 항목을 관리하기 위해 프로파일 모델 추가
#
########################################################################################################################
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="운용센터")

    class Meta:
        verbose_name = "프로파일"
        verbose_name_plural = "프로파일"