from django.db import models
from datetime import date
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length = 200 , help_text ='Enter a book Genre e.g. science Fiction , French poetry etc.')
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length = 200)
    summary = models.TextField(max_length = 1000 , help_text = 'Enter brief description of the book')
    isbn = models.CharField(max_length= 13 , help_text='13 Characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre , help_text='select genre for this book')
    author = models.ForeignKey('Author' , on_delete=models.SET_NULL , null=True)


    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True , blank=True)
    date_of_death = models.DateField('Died', null=True , blank=True)

    class Meta:
        ordering = ["last_name" , "first_name"]


    def __str__(self):
        return "{0}, {1}".format(self.last_name , self.first_name)


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , help_text='Unique ID for this particular book acorss whole library')
    book = models.ForeignKey('book', on_delete=models.SET_NULL , null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True , blank=True)
    borrower = models.ForeignKey(User , on_delete=models.SET_NULL , null=True , blank=True)

    LOAN_STATUS=(
        ('m','Maintenance'),
        ('o','On Loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(max_length=1 , choices=LOAN_STATUS , blank=True , default='m' , help_text='book availability')

    class Meta:
        ordering = ["due_back"]
        permissions = (
            ("can_read_private_section","Vip User"),
            ("user_watcher","User Watcher"),
            ("librarian","Librarian"),
        )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return "{0} ({1})".format(self.id , self.book.title)

