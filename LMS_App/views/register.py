from django.views import View
from django.shortcuts import render
from LMS_App.models.library_user import Library_User

class Register(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user=Library_User(name=name,
                  email=email,
                  password=password)
        user.save()
        register_success=True
        return render(request,'register.html',{'register_success':register_success})