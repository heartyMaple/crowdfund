from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Item, Category, Profile
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm
from django.contrib import messages
from django.contrib.auth.models import User



def items(request):
    query = request.GET.get("query", "")
    category_id = request.GET.get("category", "")
    categories = Category.objects.all()
    items = Item.objects.filter(is_over=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(
        request,
        "item/items.html",
        {
            "items": items,
            "query": query,
            "categories": categories,
            "category_id": category_id,
        },
    )


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_over=False).exclude(
        pk=pk
    )[0:3]
    return render(
        request, "item/detail.html", {"item": item, "related_items": related_items}
    )


@login_required
def new(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("item:detail", pk=item.id)
    else:
        form = NewItemForm()

    return render(request, "item/form.html", {"form": form, "title": "New Project"})


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect("dashboard:index")


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            return redirect("item:detail", pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, "item/form.html", {"form": form, "title": "Edit Project"})



@login_required
def donate_update(request, pk):
    user = get_object_or_404(User, pk=request.user.id)
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        input_number = float(request.POST.get('input_number'))
        if user and item:
            input_number = request.POST.get('input_number')
            user.profile.balance = user.profile.balance - float(input_number)
            user.save()
            messages.success(request, f'Balance updated successfully!')
            item.progress = item.progress + float(input_number)
            item.save()
            messages.success(request, f'Progress updated successfully!')
        else:
            messages.error(request, f'Failed to update progress!')
            messages.error(request, f'Failed to update progress!')
    return redirect("item:detail", pk)

@login_required
def donate(request,pk):
    item = get_object_or_404(Item, pk=pk)
    return render(
        request, "item/donate.html", {"item": item}
    )


@login_required
def over(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.is_over = True
    item.save()
    return redirect("dashboard:index")