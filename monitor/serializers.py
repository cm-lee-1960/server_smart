from rest_framework import serializers
from monitor.models import PhoneGroup, MeasuringDayClose

###################################################################################################
# 모델 직렬화 관련 모듈
# -------------------------------------------------------------------------------------------------
# 2022.03.26 - 중복코드를 최적화 하기 위해 모델 직렬화 모듈 작성
#
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 다이나믹필드 모델 직렬화 클래스
# - 특정 필드 파라미터를 받아서 해당 필드들만 보여지도록 하는 기능
# -------------------------------------------------------------------------------------------------
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """ 다이나믹필드 모델 직렬화 클래스
        - 파라미터
          . fields: 직렬화 대상 필드 리스트
        - 반환값: JSON형태
    """

    def __init__(self, *args, **kwargs):
        # 상위 클래스에는 필드 파라미터를 전달하지 않기 위해서 키워드파라미터(kwargs)에서 제거한다.
        fields = kwargs.pop('fields', None)

        # 상위클래스를 호출하여 초기화 한다.
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        # 필드 파라미터가 전달된 경우 지정되지 않는 필드 항목을 직렬화 대상에서 제외한다.
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

# -------------------------------------------------------------------------------------------------
# 단말그룹 직렬화 클래스
# -------------------------------------------------------------------------------------------------
class PhoneGroupSerializer(DynamicFieldsModelSerializer):
    """단말그룹 직렬화 글래스"""
    class Meta:
        model = PhoneGroup
        fields = '__all__' 