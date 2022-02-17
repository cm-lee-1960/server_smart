from django.shortcuts import render

# Create your views here.
def make_report(request):
    return render(request, "analysis/daily_report.html")