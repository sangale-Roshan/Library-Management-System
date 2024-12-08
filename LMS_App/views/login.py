from django.shortcuts import render,redirect
from django.views import View
from LMS_App.models.library_user import Library_User

class Login(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=Library_User.objects.get(email=email)
            if user:
                if user.password == password:
                    request.session['user']=user.name
                    request.session['id']=user.id
                    return redirect('home')

        except:
            pass
        return render(request,'login.html')
def logout(request):
    request.session.clear()
    return render(request,'login.html')