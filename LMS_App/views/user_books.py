from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from LMS_App.models.book import Book
from LMS_App.models.borrow_request import Borrow_Request
from LMS_App.models.library_user import Library_User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class BooksView(View,LoginRequiredMixin):
    def get(self, request):
        # Get the logged-in user's library user object
        library_user_id = request.session.get('id')
        if not library_user_id:
            return redirect('/login')

        library_user = get_object_or_404(Library_User, id=library_user_id)

        # Get books that are approved for the user
        approved_requests = Borrow_Request.objects.filter(user=library_user, status='approved')
        approved_books = [request.book for request in approved_requests]

        return render(request, 'user_books.html', {'approved_books': approved_books})
