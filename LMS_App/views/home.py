from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from LMS_App.models.library_user import Library_User
from LMS_App.models.book import Book
from LMS_App.models.borrow_request import Borrow_Request
from django.contrib import messages
from django.utils import timezone


class Home(View):
    def get(self, request):
        library_user_id = request.session.get('id')
        if not library_user_id:
            messages.error(request, 'You must log in first.')
            return redirect('/login')

        # Fetch the logged-in library user
        library_user = get_object_or_404(Library_User, id=library_user_id)
        books = Book.objects.all()

        # Fetch user-specific borrow requests
        user_requests = Borrow_Request.objects.filter(user=library_user)
        requested_books = {req.book.id: req for req in user_requests}

        # Get the current time
        current_time = timezone.now()

        # Update the statuses in the database for expired requests
        for borrow_request in user_requests:
            if borrow_request.status == 'approved' and borrow_request.end_date and borrow_request.end_date < current_time:
                borrow_request.status = 'expired'
                borrow_request.save()

        # Attach status info to each book for rendering and update available copies
        for book in books:
            book_request = requested_books.get(book.id)
            if book_request:
                book.status = book_request.status
            else:
                book.status = None

            # Calculate the number of approved borrow requests for the book
            approved_borrows = Borrow_Request.objects.filter(book=book, status='approved').count()

            # Update available copies based on the borrow requests
            # If the number of borrow requests equals or exceeds the available copies, set available copies to 0
            if book.copies_available - approved_borrows <= 0:
                book.copies_available = 0  # No copies available
            else:
                book.copies_available = book.copies_available - approved_borrows  # Update available copies

        data = {
            'books': books,
        }
        return render(request, 'home.html', data)

    def post(self, request):
        library_user_id = request.session.get('id')
        if not library_user_id:
            messages.error(request, 'You must log in first.')
            return redirect('/login')

        library_user = get_object_or_404(Library_User, id=library_user_id)
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        # Calculate the number of approved borrow requests for the book
        approved_borrows = Borrow_Request.objects.filter(book=book, status='approved').count()

        # Check if the book is already borrowed (i.e., all copies are taken)
        if book.copies_available - approved_borrows <= 0:
            messages.warning(request, "This book is currently being read by another user. You cannot borrow it right now.")
        else:
            # Check if the user already has an active borrow request for this book
            existing_borrow_request = Borrow_Request.objects.filter(user=library_user, book=book).first()

            if existing_borrow_request:
                current_time = timezone.now()

                # If the previous borrow request is expired, allow a new request
                if (
                    existing_borrow_request.status == 'approved' and
                    existing_borrow_request.end_date and
                    existing_borrow_request.end_date < current_time
                ):
                    Borrow_Request.objects.create(user=library_user, book=book)
                    messages.success(request, "Your request has been submitted again for the expired book.")
                elif existing_borrow_request.status == 'expired':
                    Borrow_Request.objects.create(user=library_user, book=book)
                    messages.success(request, "Your request has been submitted again for the expired book.")
                else:
                    # If the request is not expired, prevent the user from requesting the same book again
                    messages.error(request, "You have already requested this book.")
            else:
                # Create a new borrow request if no request exists for this book
                Borrow_Request.objects.create(user=library_user, book=book)
                messages.success(request, "Your request has been submitted.")

        return redirect('/')
