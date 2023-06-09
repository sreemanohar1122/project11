from django.shortcuts import render
from django.views import View
import requests
import random
from django.core.mail import send_mail
from django.http import HttpResponse
from project11.settings import EMAIL_HOST_USER
from .forms import RegForm
from .models import RegModel
# Create your views here.
class Home(View):
    def get(self,request):
        rf=RegForm()
        con_dic={'rf':rf}
        return render(request,'home.html',context=con_dic)
class Reg(View):
    def post(self,request):
        otp=str(random.randint(10000000,99999999))
        print(otp)
        mobno=request.POST["MobileNo"]
        emailid=request.POST["Emailid"]
        resp = requests.post('https://textbelt.com/text', {
            'phone': mobno,
            'message': otp,
            'key': 'deb651692eabe6a8c4dc2bf4c540d840302c14beufATt5cvEXUzaN5EDcNM17S9q',
        })
        print(resp.json())
        send_mail("otp for registration", otp, EMAIL_HOST_USER, [emailid], fail_silently=True)
        rf = RegForm(request.POST)
        if rf.is_valid():
            rm=RegModel(Fname=rf.cleaned_data["FirstName"],
                        Lname=rf.cleaned_data["LastName"],
                        Uname=rf.cleaned_data['UserName'],
                        Password=rf.cleaned_data['Password'],
                        Cpassword=rf.cleaned_data['CPassword'],
                        Email=rf.cleaned_data['Emailid'],
                        Mobno=rf.cleaned_data['MobileNo'])
            rm.save()
            return HttpResponse("reg success")
# Create your views here.
