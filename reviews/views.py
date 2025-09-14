from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review
from .forms import ReviewForm, BookForm


def home(request):
    return render(request, "reviews/home.html")

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    return render(request, "reviews/book_detail.html", {"book": book, "reviews": reviews})

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = Book(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data['image']
            )
            book.save()
            return redirect("book_view", pk=book.pk)
    else:
        form = BookForm()
    return render(request, "reviews/add_book.html", {"form": form})

def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("book_view", pk=review.book.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/edit_review.html", {"form": form, "review": review, "book": book})

def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    book_pk = review.book.pk
    review.delete()
    return redirect("book_view", pk=book_pk)