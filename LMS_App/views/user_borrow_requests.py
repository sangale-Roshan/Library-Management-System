from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from LMS_App.models.borrow_request import Borrow_Request
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from LMS_App.models.library_user import Library_User
from django.utils import timezone
print(timezone.now())

class BorrowRequestsView(View,LoginRequiredMixin):
    def get(self, request):
        library_user_id = request.session.get('id')
        if not library_user_id:
            return redirect('/login')
        print(timezone.now())

        library_user = get_object_or_404(Library_User, id=library_user_id)
        borrow_requests = Borrow_Request.objects.filter(user=library_user).exclude(status='approved')

        return render(request, 'user_borrow_requests.html', {'borrow_requests': borrow_requests})
