from django.contrib import admin
from .models.library_user import Library_User
from .models.book import Book
from .models.borrow_request import Borrow_Request

# Register your models here.
admin.site.register(Library_User)
admin.site.register(Book)
admin.site.register(Borrow_Request)

