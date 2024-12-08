from django.db import models
from django.template.defaulttags import now

from .library_user import Library_User
from .book import Book


class Borrow_Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected')
    ]

    user = models.ForeignKey(Library_User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    requested_time = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)  # Date when book is approved
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.name} - {self.book.title} ({self.status})'

    def is_expired(self):
        """Check if the borrow period has expired."""
        return self.end_date and now() > self.end_date
