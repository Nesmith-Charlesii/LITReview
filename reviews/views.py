from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review


def home(request):
    return render(request, "reviews/home.html")

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    return render(request, "reviews/book_detail.html", {"book": book, "reviews": reviews})