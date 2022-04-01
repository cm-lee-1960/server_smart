from rest_framework import serializers, relations
from monitor.models import Phone, PhoneGroup, MeasuringDayClose
from management.models import Center, Morphology

########################################################################################################################
# 모델 직렬화 관련 모듈
#  ┌ -----------------------------┐   ┌ ------------------┐ <has a>   ┌ -------------------┐
#  | DynamicFieldsModelSerializer |   | IdModelSerializer |------┯--->| IdManyRelatedField |
#  | (직렬화시 필드 지정 가능)    |   | (관계 필드 '_id   |      |    └------------------- ┘
#  └--------------┯-------------- ┘   └---------┯-------- ┘      |    ┌ -------------------┐
#                 |                             |                └--->| IdManyRelatedField |
#                 |                             |                     └------------------- ┘
#                 └--------------┯--------------┘
#                                |
#                   ┌ -----------∨---------┐
#                   | PhoneGroupSerializer | [ 기능 ]
#                   |                      |  * 모델을 직렬활할 때 특정 필드만 선택하여 직렬화 가능
#                   └--------------------- ┘  * 관계 필드가 포함된 경우 '_id'로 직렬화 가능
#                                               (예: center_id, morphology_id 등)
# [ 사용법 ]
# fields = ['center_id', 'morphology_id', 'measdate', 'userInfo1', 'networkId', 'downloadBandwidth', 'uploadBandwidth',
#                'dl_count', 'ul_count', 'dl_nr_count', 'ul_nr_count', 'dl_nr_percent', 'ul_nr_percent', 'total_count']
# serializer = PhoneGroupSerializer(phoneGroup, fields=fields)
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.26 - 중복코드를 최적화 하기 위해 모델 직렬화 모듈 작성
# 2022.04.01 - 모델 내에 관계 필드를 '_ids' 또는 '_id'를 붙이는 클래스 오류 수정
#
########################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
# 모델 직렬화 시 외부키(Foreign Key)에 _ids 또는 _id 서핏스를 붙여주는 모들
# ----------------------------------------------------------------------------------------------------------------------
class IdManyRelatedField(relations.ManyRelatedField):
    """관계 필드에 서픽스 '_ids'를 붙이기 위한 클래스"""
    field_name_suffix = '_ids'

    def bind(self, field_name, parent):
        self.source = field_name[:-len(self.field_name_suffix)]
        super().bind(field_name, parent)

class IdPrimaryKeyRelatedField(relations.PrimaryKeyRelatedField):
    """관계 필드에 서픽스 '_id'를 붙이기 위한 클래스"""
    many_related_field_class = IdManyRelatedField
    field_name_suffix = '_id'

    def bind(self, field_name, parent):
        if field_name:
            self.source = field_name[:-len(self.field_name_suffix)]
        super().bind(field_name, parent)

class IdModelSerializer(serializers.ModelSerializer):
    """모델 내에 관계 필드가 있는 경우 'FIELD_NAME_id' 변경하는 클래스"""
    serializer_related_field = IdPrimaryKeyRelatedField

    def get_fields(self):
        fields = super().get_fields()
        new_fields = type(fields)()

        for field_name, field in fields.items():
            try:
                field_name += field.field_name_suffix
            except AttributeError:
                pass
            new_fields[field_name] = field

        return new_fields

# ----------------------------------------------------------------------------------------------------------------------
# 다이나믹필드 모델 직렬화 클래스
# - 특정 필드 파라미터를 받아서 해당 필드들만 보여지도록 하는 기능
# ----------------------------------------------------------------------------------------------------------------------
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

########################################################################################################################
# 단말그룹 직렬화 클래스
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.26 - IdModelSerializer가 Foreign Key를 _id를 붙여주는 좋은 코드인데, 정상동작 하지 않음
# 2022.04.01 - @property decorator 항목 직렬화 추가
#
########################################################################################################################
class PhoneGroupSerializer(IdModelSerializer, DynamicFieldsModelSerializer):
# class PhoneGroupSerializer(DynamicFieldsModelSerializer):
    """단말그룹 직렬화 글래스"""
    # 2022.04.01 - IdModelSerializer 클래스를 상속하면서 불필요한 코드가 됨
    #            - 그래도 향후 사용하거나 참고하기 위해 코드를 남겨 두는 것이 좋을 듯 함
    # center_id = serializers.ReadOnlyField(source = 'center.id') # 운용센터
    # centerName = serializers.ReadOnlyField(source = 'center.centerName') # 운용센터명
    # center = CenterSerializer(many=False, read_only=True)
    # morphology_id = serializers.ReadOnlyField(source = 'mSorphology.id') # 모폴로지
    # p_measuringTeam = serializers.ReadOnlyField() # 금일 측정조 (@property decorator)

    class Meta:
        model = PhoneGroup
        fields = '__all__'


########################################################################################################################
# 측정단말 직렬화 클래스
# ----------------------------------------------------------------------------------------------------------------------
########################################################################################################################
class PhoneSerializer(DynamicFieldsModelSerializer):
    """측정다말 직렬화 글래스"""
    # 2022.04.01 - IdModelSerializer 클래스를 상속하면서 불필요한 코드가 됨
    #            - 그래도 향후 사용하거나 참고하기 위해 코드를 남겨 두는 것이 좋을 듯 함
    # phoneGroup_id = serializers.ReadOnlyField(source = 'phoneGroup.id') # 단말그룹
    # center_id = serializers.ReadOnlyField(source = 'center.id') # 운용센터
    # morphology_id = serializers.ReadOnlyField(source = 'morphology.id') # 모폴로지

    class Meta:
        model = Phone
        fields = '__all__'
