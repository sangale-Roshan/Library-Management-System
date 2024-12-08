from django.shortcuts import render, get_object_or_404, redirect
from LMS_App.models.book import Book
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from LMS_App.models.library_user import Library_User
from LMS_App.models.borrow_request import Borrow_Request


@method_decorator(login_required, name='dispatch')
class ReadBook(View):
    def get(self, request, book_id):
        library_user_id = request.session.get('id')
        if not library_user_id:
            messages.error(request, 'You must login first')
            return redirect('/login')

        library_user = get_object_or_404(Library_User, id=library_user_id)
        book = get_object_or_404(Book, id=book_id)

        # Check if the user has an approved request
        approved_request = Borrow_Request.objects.filter(user=library_user, book=book, status='approved').exists()
        if not approved_request:
            messages.error(request, "You do not have permission to read this book.")
            return redirect('/')

        # Render the read page (use an iframe or inline viewer for books)
        return render(request, 'read_book.html',{'book':book})