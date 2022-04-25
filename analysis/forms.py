from django import forms
from .models import MeasLastyear5G, MeasLastyearLTE



# -------------------------------------------------------------------------------------------------
# 사후측정결과 등록 및 수정(5G) 하기 위한 폼
# -------------------------------------------------------------------------------------------------
# class PostMeasure5GForm(forms.ModelForm):
#     class Meta:
#         model = PostMeasure5G
#         fields = "__all__"

#     # 폼(Form)의 모든 필드는 기본값으로 required가 True라서 False로 처리한다.
#     def __init__(self, *args, **kwargs):
#         super(PostMeasure5GForm, self).__init__(*args, **kwargs)
#         for field_name in self.fields.keys():
#             self.fields[field_name].required = False


# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(5G) 하기 위한 폼
# -------------------------------------------------------------------------------------------------
class MeasLastyear5GForm(forms.ModelForm):
    class Meta:
        model = MeasLastyear5G
        fields = "__all__"

    # 폼(Form)의 모든 필드는 기본값으로 required가 True라서 False로 처리한다.
    def __init__(self, *args, **kwargs):
        super(MeasLastyear5GForm, self).__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].required = False

# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(LTE) 하기 위한 폼
# -------------------------------------------------------------------------------------------------
class MeasLastyearLTEForm(forms.ModelForm):
    class Meta:
        model = MeasLastyearLTE
        fields = "__all__"

    # 폼(Form)의 모든 필드는 기본값으로 required가 True라서 False로 처리한다.
    def __init__(self, *args, **kwargs):
        super(MeasLastyearLTEForm, self).__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].required = False