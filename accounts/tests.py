# ###########################################################################################
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token


# @receiver(post_save, senders=settings.AUTH_USER_MODEL)
# def create_auth_token(sener, instance=None, created=False, **kwargs):
# 	if created:	# create/update 모두 save 이므로, created 일때만 token을 생성하게 한다.
#     	Token.objects.create(user=instance)
#         #Token.save()