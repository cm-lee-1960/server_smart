from rest_framework import serializers
from .models import PhoneGroup

# -------------------------------------------------------------------------------------------------
# 단말그룹 직렬화 클래스 -- 작성중
# -------------------------------------------------------------------------------------------------
class PhoneGroupSerializer(serializers.Serializer):

    fields = "__all__"

    class Meta:
        model = PhoneGroup


    def __init__(self, *args, **kwargs):
        super(PhoneGroupSerializer, self).__init__(*args, **kwargs)
        # 타겟 오브젝트가 있으면 타겟 오브젝트가 갖고 있는 필드를 대상으로 한다.
        if 'targetObject' in kwargs:
            self.fields = kwargs['targetObject']._meta.fields

        super().__init__(*args, **kwargs)
