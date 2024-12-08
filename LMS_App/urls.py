"""
URL configuration for LMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views.home import Home
from .views.register import Register
from .views.login import Login
from .views.login import logout
from .views.readbook import ReadBook
from .views.user_books  import BooksView
from .views.user_borrow_requests import BorrowRequestsView
from .views.user_borrow_history import BorrowHistoryView
from .views.download_borrow_history import DownloadBorrowHistory
from LMS import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home.as_view(),name='home'),
    path('register/',Register.as_view(),name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('read_book/<int:book_id>/', ReadBook.as_view(), name='read_book'),
    path('my_books/', BooksView.as_view(), name='my_books'),
    path('my_borrow_requests/', BorrowRequestsView.as_view(), name='my_borrow_requests'),
    path('my_borrow_history/', BorrowHistoryView.as_view(), name='my_borrow_history'),
    path('download_borrow_history/', DownloadBorrowHistory.as_view(), name='download_borrow_history'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
