from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review


def home(request):
    return render(request, "reviews/home.html")

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    return render(request, "reviews/book_detail.html", {"book": book, "reviews": reviews})

def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        review.headline = request.POST.get("headline")
        review.body = request.POST.get("body")
        review.rating = request.POST.get("rating")
        review.save()
        return redirect("book_view", pk=review.book.pk)
    return render(request, "reviews/edit_review.html", {"review": review})

def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    book_pk = review.book.pk
    review.delete()
    return redirect("book_view", pk=book_pk)