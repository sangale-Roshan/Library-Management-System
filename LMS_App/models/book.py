from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    image=models.ImageField(upload_to='media/book_images/')
    copies_available = models.PositiveIntegerField(default=1)
    file=models.FileField(upload_to='media/book_files/')

    def __str__(self):
        return self.title