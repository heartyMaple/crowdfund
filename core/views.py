from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignupForm
from django.contrib.auth.models import User
from django.db.models import Sum



def index(request):
    user_count = User.objects.count()
    item_count = Item.objects.count()
    progress_count = Item.objects.aggregate(progress_count=Sum('progress'))['progress_count']
    items = Item.objects.filter(is_over=False)[0:6]
    categories = Category.objects.all()
    

    return render(
        request,
        "core\index.html",
        {
            "categories": categories,
            "items": items,
            "user_count": user_count,
            "progress_count": progress_count,
            "item_count": item_count,
            
        },
    )


def contact(request):
    return render(request, "core\contact.html")

def about(request):
    return render(request, "core/about.html")

def privacy_policy(request):
    return render(request, "core/privacy_policy.html")

def term_of_use(request):
    return render(request, "core/term_of_use.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect("/login/")
    else:
        form = SignupForm()
    return render(request, "core/signup.html", {"form": form})

