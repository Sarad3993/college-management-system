from django.shortcuts import render

# Create your views here.


def hello_view(request):
    return render(request,'college/hello.html')
