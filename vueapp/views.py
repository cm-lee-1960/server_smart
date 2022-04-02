from django.shortcuts import render
from django.views.generic import TemplateView
from monitor.models import PhoneGroup

# Create your views here.
class  DashboardVue(TemplateView):
    template_name = 'vueapp/dashboard_form.html'

    # def get(self, request, *args, **kwargs):
    #         phoneGroup_list = PhoneGroup.objects.all()
    #         context = {'phoneGroup_list': phoneGroup_list}
    #         return render(request, "vueapp/dashboard_form.html", context=context)

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardVue, self).get_context_data(*args, **kwargs)
        context['phoneGroup_list'] = PhoneGroup.objects.all()
        return context