from django.shortcuts import render

def donate_view(request):
    return render(request, "donations/donate.html")
