from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginUserForm, AddWineForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Rating, User, Wine
import math


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
            wine = Wine.objects.get(pk=id)

            dic = request.session["cart"]

            if request.method == "POST":
                qty = int(request.POST["product_" + str(id)])
                print(qty, wine.in_stock)
                if qty > wine.in_stock:
                    messages.error(request, "Podana liczba przekracza dostępną ilość produktu!", extra_tags='too_much')
                else:
                    dic[str(id)] = qty
                    request.session["cart"] = dic

            price = dic[str(id)] * float(wine.price)
            whole_products.append([wine, dic[str(id)], price])
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

    wine = Wine.objects.get(pk=wine_id)
    wine_quantity = wine.in_stock

    print(wine_id, request.session["cart"].keys())
    if str(wine_id) not in request.session["cart"].keys():
        print("New wine")
        request.session["cart"][str(wine_id)] = 0

    dic = request.session["cart"]
    if dic[str(wine_id)] >= wine_quantity:
        return redirect("home")

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
    print(logged_user)
    is_admin = check_if_admin(logged_user)

    chosen_wine = Wine.objects.get(pk=wine_id)

    wine_rates = [rating.rate for rating in Rating.objects.filter(author_id=logged_user.user_uid, wine_id=wine_id) ]

    rate_len = len(wine_rates)
    if rate_len:
        mean_rate = sum(wine_rates) / rate_len
    else:
        mean_rate = 0
    mean_rate = round(mean_rate, 1)
    decimal_part = mean_rate - math.floor(mean_rate)

    rate = 0

    if "cart" not in request.session:
        print("New cart session")
        request.session["cart"] = {}

    if "cart" in request.session:
        if request.method == "POST":
            if str(wine_id) not in request.session["cart"].keys():
                request.session["cart"][str(wine_id)] = 0

            for id, qty in request.session["cart"].items():
                if "product_num" in request.POST:
                    qty = int(request.POST["product_num"])

                    dic = request.session["cart"]

                    if dic[str(wine_id)] + qty > chosen_wine.in_stock:
                        messages.error(request, "Podana liczba przekracza dostępną ilość produktu!", extra_tags='too_much')
                        break
                    else:
                        dic[str(id)] += qty
                        request.session["cart"] = dic

            if "rate" in request.POST:
                rate = request.POST["rate"]

            if rate:
                desc = request.POST["rate-message"]
                Rating.objects.update_or_create(wine_id=wine_id, author_id=logged_user.user_uid, rate=rate, description=desc)
            return redirect("wine_page", wine_id)

    items_in_cart = get_cart_items_number(request)
    print(decimal_part)

    data = {
        "is_logged": is_logged,
        "wine": chosen_wine,
        "items_in_cart": items_in_cart,
        "is_admin": is_admin,
        "logged_user": logged_user,
        "rate_len": rate_len,
        "mean_rate": mean_rate,
        "decimal_part": decimal_part,
        "star_range": range(1,5 + 1)
    }
    return render(request, "ordering_website/wine_page.html", data)


def add_wine_page(request):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    if not is_admin:
        return redirect("home")

    items_in_cart = get_cart_items_number(request)

    if request.method == "POST":
        form = AddWineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            current_wine = form.cleaned_data.get("wine")
            messages.success(request, "Wine was created successfully", extra_tags="wine_created")
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


def update_wine_page(request, wine_id):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    items_in_cart = get_cart_items_number(request)

    if not is_admin:
        return redirect("home")

    wine = Wine.objects.get(pk=wine_id)
    form = AddWineForm(instance=wine)

    if request.method == "POST":
        form = AddWineForm(request.POST, request.FILES, instance=wine)
        if form.is_valid():
            form.save()
            messages.success(request, "Wine was updated successfully", extra_tags="wine_updated")
            return redirect("wine_page", wine_id)

    data = {
        "is_logged": is_logged,
        "is_admin": is_admin,
        "form": form,
        "items_in_cart": items_in_cart,
        "logged_user": logged_user,
    }
    return render(request, "ordering_website/update_wine_page.html", data)


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


