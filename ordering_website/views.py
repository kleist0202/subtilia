from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginUserForm, AddWineForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import User, Wine


def home(request):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    items_in_cart = get_cart_items_number(request)

    wines = Wine.objects.all()

    data = {
        "is_logged": is_logged,
        "wines": wines,
        "items_in_cart": items_in_cart,
        "is_admin": is_admin,
        "logged_user": logged_user,
    }
    return render(request, "ordering_website/home.html", data)


def registration_page(request):
    if "email" in request.session:
        return redirect("home")

    items_in_cart = get_cart_items_number(request)

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            current_username = form.cleaned_data.get("username")
            print(current_username)
            messages.success(request, "Account was created successfully")
            return redirect("login")
    else:
        form = CreateUserForm()

    data = {"form": form, "items_in_cart": items_in_cart}

    return render(request, "ordering_website/registration_page.html", data)


def login_page(request):
    if "email" in request.session:
        return redirect("home")

    items_in_cart = get_cart_items_number(request)

    form = LoginUserForm()
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session["email"] = user.email
                return redirect("home")
            else:
                messages.error(request, "Invalid password for email: " + user.email)
        else:
            messages.error(request, "There is no such account")

    data = {"form": form, "items_in_cart": items_in_cart}

    return render(request, "ordering_website/login_page.html", data)


def logout(request):
    if "email" in request.session:
        del request.session["email"]
    return redirect("login")


def profile(request):
    if "email" not in request.session:
        return redirect("home")

    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    items_in_cart = get_cart_items_number(request)

    if request.method == "POST":
        name = request.POST["name"]
        surname = request.POST["surname"]
        adrress = request.POST["adr"]
        city = request.POST["city"]
        phone = request.POST["phone"]
        zip = request.POST["zip"]

        current_user_email = get_user(request)[0].email
        _ = User.objects.filter(email=current_user_email).update(
            name=name,
            surname=surname,
            address_and_number=adrress,
            city=city,
            phone_number=phone,
            zip_code=zip,
        )
        logged_user, _ = get_user(request)

        messages.success(request, "Dane zostały zaktualizowane.")

    data = {
        "is_logged": is_logged,
        "items_in_cart": items_in_cart,
        "is_admin": is_admin,
        "logged_user": logged_user,
    }

    return render(request, "ordering_website/profile.html", data)


def cart_page(request):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    cart_products = []
    whole_products = []
    total_price = 0
    sum_price = 0

    qty = 1

    if "cart" in request.session:
        for id, qty in request.session["cart"].items():
            if request.method == "POST":
                qty = request.POST["product_" + str(id)]

                dic = request.session["cart"]
                dic[str(id)] = int(qty)
                request.session["cart"] = dic

            cp = Wine.objects.get(pk=id)
            price = int(qty) * float(cp.price)
            whole_products.append([cp, qty, price])
            sum_price += price

    total_price = round(float(sum_price) + 9.99, 2)

    items_in_cart = get_cart_items_number(request)

    data = {
        "is_logged": is_logged,
        "whole_products": whole_products,
        "items_in_cart": items_in_cart,
        "sum_price": sum_price,
        "total_price": total_price,
        "is_admin": is_admin,
        "logged_user": logged_user,
    }
    return render(request, "ordering_website/cart_page.html", data)


def add_to_cart(request, wine_id):
    # del request.session["cart"]
    if "cart" not in request.session:
        print("New session")
        request.session["cart"] = {}

    print(wine_id, request.session["cart"].keys())
    if str(wine_id) not in request.session["cart"].keys():
        print("New wine")
        request.session["cart"][str(wine_id)] = 0

    dic = request.session["cart"]
    dic[str(wine_id)] += 1
    request.session["cart"] = dic
    print(request.session["cart"])

    return redirect("home")


def remove_from_cart(request, wine_id):
    if "cart" in request.session:
        dic = request.session["cart"]
        dic.pop(str(wine_id))
        request.session["cart"] = dic

    return redirect("cart_page")


def wine_page(request, wine_id):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    chosen_wine = Wine.objects.get(pk=wine_id)
    print(chosen_wine.name)

    items_in_cart = get_cart_items_number(request)

    data = {
        "is_logged": is_logged,
        "wine": chosen_wine,
        "items_in_cart": items_in_cart,
        "is_admin": is_admin,
        "logged_user": logged_user,
    }
    return render(request, "ordering_website/wine_page.html", data)


def add_wine_page(request):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    items_in_cart = get_cart_items_number(request)

    if request.method == "POST":
        form = AddWineForm(request.POST, request.FILES)
        if form.is_valid():
            print("DZXIALA")
            form.save()
            current_wine = form.cleaned_data.get("wine")
            print(current_wine)
            messages.success(request, "Wine was created successfully")
            return redirect("add_wine_page")
    else:
        form = AddWineForm()

    data = {
        "is_logged": is_logged,
        "is_admin": is_admin,
        "form": form,
        "items_in_cart": items_in_cart,
        "logged_user": logged_user,
    }

    return render(request, "ordering_website/add_wine_page.html", data)


# ------------------ useful functions ---------------------


def check_if_admin(logged_user):
    is_admin = False

    if logged_user is None:
        return is_admin

    if logged_user.rank == "admin":
        is_admin = True

    return is_admin


def get_user(request):
    if "email" in request.session:
        return User.objects.get(email=request.session["email"]), True

    return None, False


def get_cart_items_number(request):
    if "cart" not in request.session:
        return 0

    items = 0
    for _, k in request.session["cart"].items():
        items += k
    return items


