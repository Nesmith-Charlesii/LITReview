from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review
from .forms import ReviewForm, BookForm


def home(request):
    if request.user.is_authenticated:
        followed_users = request.user.following.all()
        reviews = Review.objects.filter(user__in=followed_users).order_by('-created')
        show_all_reviews_link = True
    else:
        reviews = Review.objects.all().order_by('-created')
        show_all_reviews_link = False

    return render(
        request,
        "reviews/home.html",
        {
            "reviews": reviews,
            "show_all_reviews_link": show_all_reviews_link,
        }
    )

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

def post_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(
                book=book,
                content=form.cleaned_data['content'],
                rating=form.cleaned_data['rating']
            )
            review.save()
            return redirect("book_view", pk=book.pk)
    else:
        form = ReviewForm()
    return render(request, "reviews/post_review.html", {"form": form, "book": book})

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