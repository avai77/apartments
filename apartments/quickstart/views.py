from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializer import UserSerializer, GroupSerializer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import PostForm

from forms import SignupForm, SigninForm
from models import Advertisement, Category
from serializer import ProductSerializer

class UserViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.

def home(request):
    products = Advertisement.objects.filter(active=True)
    categories = Advertisement.objects.filter(active=True)
    context = {"products": products, "categories": categories}
    return render(request, "shop/home.html", context)


def product_add(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.model_pic = form.cleaned_data['image']
            post.save()
            return redirect('/', pk=post.pk)

    elif request.user.is_authenticated:
        form = PostForm()
        return render(request, 'shop/post_edit.html', {'form': form})
    else:
        return render(request, 'shop/error.html')


def product_edit(request, pk):
    post = get_object_or_404(Advertisement, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('detail', pk=Advertisement.pk)
    else:
        form = PostForm(instance=Advertisement)
    return render(request, 'shop/post_edit.html', {'form': form})



def search(request):
    q = request.GET["q"]
    products = Advertisement.objects.filter(active=True, name__icontains=q)
    categories = Category.objects.filter(active=True)
    context = {"products": products,
               "categories": categories,
               "title": q + " - search"}
    return render(request, "shop/list.html", context)


def categories(request, slug):
    cat = Category.objects.get(slug=slug)
    products = Advertisement.objects.filter(active=True, category=cat)
    categories = Category.objects.filter(active=True)
    context = {"products": products, "categories": categories, "title": cat.name + " - Categories"}
    return render(request, "shop/list.html", context)


def detail(request, slug):
    product = Advertisement.objects.get(active=True, slug=slug)

    categories = Category.objects.filter(active=True)
    context = {"product": product,
               "categories": categories,
               }
    return render(request, "shop/detail.html", context)




def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "User saved")
            return redirect("shop:signin")
        else:
            messages.error(request, "Error in form")
    else:
        form = SignupForm()
    context = {"form": form}
    return render(request, "shop/signup.html", context)


def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        # username = req.POST["username"]
        # password = req.POST["password"]
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("shop:home")
        else:
            messages.error(request, "Invalid Username or Password")
    else:
        form = SigninForm()
    context = {"form": form}
    return render(request, "shop/signin.html", context)


def signout(request):
    logout(request)
    return redirect("shop:signin")

