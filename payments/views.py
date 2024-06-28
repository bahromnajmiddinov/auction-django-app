from django.shortcuts import render


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')
