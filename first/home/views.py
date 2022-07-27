import re
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # return HttpResponse("<marquee><h1>This is our first django app<h1></marquee>")
    # return render(request,'index.html')
    # return render(request,'index.html',{'name':'Arcgate, Udaipur'})
    return render(request,'index.html',{'name':'this','data':'[11,12,13,14]'})

def calc(request):
    a=request.GET['n1']
    b=request.GET['n2']
    ch=request.GET['ch']
    a=int(a)
    b=int(b)
    c=0
    if ch=='Add':
        c=a+b
    elif ch=='sub':
        c=a-b
    elif ch=='mul':
        c=a*b
    elif ch=='div':
        try:
            c=a/b
        except ZeroDivisionError:
            c="unable to zero division error"
    return render(request,'result.html',{'result':c})

def calculator(request):
    val=request.POST['val']
    return render(request,'result.html',{'result':eval(val)})
    