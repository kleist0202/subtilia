from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import CreateUserForm, LoginUserForm, AddWineForm, RatingForm, SubmitOrderForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import OrderData, OrderedProduct, Rating, User, Wine
import math


def home(request):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    items_in_cart = get_cart_items_number(request)

    rating_dict = {}

    wines = Wine.objects.all()

    for wine in wines:
        wine_rates = [rating.rate for rating in Rating.objects.filter(wine_id=wine.wine_id) ]

        rate_len = len(wine_rates)
        if rate_len:
            mean_rate = sum(wine_rates) / rate_len
        else:
            mean_rate = 0
        mean_rate = round(mean_rate, 1)
        decimal_part = mean_rate - math.floor(mean_rate)
        rating_dict[wine.wine_id] = [rate_len, mean_rate, decimal_part]

    data = {
        "is_logged": is_logged,
        "wines": wines,
        "items_in_cart": items_in_cart,
        "is_admin": is_admin,
        "logged_user": logged_user,
        "rating_dict": rating_dict,
        "star_range": range(1,5 + 1)
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

    whole_products = []
    sum_price = 0

    qty = 1

    if "cart" in request.session:
        for id, qty in request.session["cart"].items():
            wine = Wine.objects.get(pk=id)

            dic = request.session["cart"]

            if request.method == "POST":
                qty = int(request.POST["product_" + str(id)])
                if qty > wine.in_stock:
                    messages.error(request, "Podana liczba przekracza dostępną ilość produktu!", extra_tags='too_much')
                else:
                    dic[str(id)] = qty
                    request.session["cart"] = dic

            price = dic[str(id)] * float(wine.price)
            whole_products.append([wine, dic[str(id)], price])
            sum_price += price

    items_in_cart = get_cart_items_number(request)

    data = {
        "is_logged": is_logged,
        "whole_products": whole_products,
        "items_in_cart": items_in_cart,
        "sum_price": sum_price,
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
    is_admin = check_if_admin(logged_user)

    chosen_wine = Wine.objects.get(pk=wine_id)

    wine_rates_objs = [rating for rating in Rating.objects.select_related('author').filter(wine_id=wine_id) ][0:5]
    wine_rates_values = [rating.rate for rating in wine_rates_objs ]

    rate_len = len(wine_rates_values)
    print(wine_rates_values)
    if rate_len:
        mean_rate = sum(wine_rates_values) / rate_len
    else:
        mean_rate = 0
    mean_rate = round(mean_rate, 1)
    decimal_part = mean_rate - math.floor(mean_rate)

    rate = 0
    rate_posted = False
    form = RatingForm()

    if is_logged:
        current_user_rate = Rating.objects.filter(author_id=logged_user.user_uid, wine_id=wine_id)
        if current_user_rate:
            rate_posted = True

    if "cart" not in request.session:
        print("New cart session")
        request.session["cart"] = {}

    if "cart" in request.session:
        print(Wine.objects.get(pk=wine_id).name)
        if request.method == "POST":
            if str(wine_id) not in request.session["cart"].keys():
                request.session["cart"][str(wine_id)] = 0

            # for id, qty in request.session["cart"].items():
            if "product_num" in request.POST:
                qty = int(request.POST["product_num"])
                print(qty)

                dic = request.session["cart"]

                if dic[str(wine_id)] + qty > chosen_wine.in_stock:
                    messages.error(request, "Podana liczba przekracza dostępną ilość produktu!", extra_tags='too_much')
                else:
                    dic[str(wine_id)] += qty
                    request.session["cart"] = dic
                    return redirect("wine_page", wine_id)

            if "rate" in request.POST:
                rate = request.POST["rate"]

            if rate:
                form = RatingForm(request.POST)

                if form.is_valid():
                    desc = form.cleaned_data.get("description")
                    # desc = request.POST["rate-message"]
                    Rating.objects.update_or_create(wine_id=wine_id, author_id=logged_user.user_uid, rate=rate, description=desc)
                    return redirect("wine_page", wine_id)

    items_in_cart = get_cart_items_number(request)
    total_obj = Rating.objects.filter(wine_id=wine_id).count()

    data = {
        "is_logged": is_logged,
        "wine": chosen_wine,
        "items_in_cart": items_in_cart,
        "is_admin": is_admin,
        "logged_user": logged_user,
        "rate_len": rate_len,
        "mean_rate": mean_rate,
        "decimal_part": decimal_part,
        "rate_posted": rate_posted,
        "rate_objs": wine_rates_objs,
        "total_obj": total_obj,
        "form": form,
        "star_range": range(1,5 + 1)
    }
    return render(request, "ordering_website/wine_page.html", data)


def load_more(request, wine_id):
    loaded_items = int(request.GET.get('loaded_items'))
    limit = 5
    rate_objs = list(
        Rating.objects.select_related('author')
        .filter(wine_id=wine_id)
        .values("rate", "wine_id", "description", "author_id", "author__name", "author__surname")[loaded_items:loaded_items + limit])
    data = {'rate_objs': rate_objs}
    return JsonResponse(data=data)


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


def checkout_page(request):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)
    sum_price = 0
    total_price = 0
    whole_products = []

    items_in_cart = get_cart_items_number(request)

    if not items_in_cart:
        return redirect("home")

    if "cart" in request.session:
        for id, qty in request.session["cart"].items():
            wine = Wine.objects.get(pk=id)

            dic = request.session["cart"]

            price = dic[str(id)] * float(wine.price)
            whole_products.append([wine, dic[str(id)], price, qty])
            sum_price += price

    if request.method == "POST":
        form = SubmitOrderForm(request.POST)

        if form.is_valid():
            email = request.POST["email"]
            name = request.POST["name"]
            surname = request.POST["surname"]
            adr = request.POST["address_and_number"]
            phone = request.POST["phone_number"]
            city = request.POST["city"]
            zip = request.POST["zip_code"]
            delivery = request.POST["delivery"]
            payment = request.POST["payment"]
            print(email, name, surname, adr, phone, city, zip, payment)

            order = OrderData(
                name=name,
                surname=surname,
                email=email,
                city=city,
                phone_number=phone,
                zip_code=zip,
                address_and_number=adr,
                delivery=delivery,
                payment=payment,
            )
            order.save()

            # add bought products to database with order id
            print([(id, qty) for id, qty in request.session["cart"].items()])
            for id, qty in request.session["cart"].items():
                wine = Wine.objects.get(pk=id)
                print(id, qty, wine.name)

                if wine.in_stock < 0:
                    print("Not enough wine")
                    continue

                dic = request.session["cart"]
                ordered_product = OrderedProduct(order=order, wine=wine, quantity=qty)
                ordered_product.save()

                # reduce the number of wines
                wine.in_stock -= qty

                wine.save(update_fields=["in_stock"])

            del request.session["cart"]

            return redirect("home")

    else:
        form = SubmitOrderForm(instance=logged_user)

    total_price = round(float(sum_price) + 9.99, 2)

    data = {
        "is_logged": is_logged,
        "is_admin": is_admin,
        "items_in_cart": items_in_cart,
        "total_price": total_price,
        "whole_products": whole_products,
        "sum_price": sum_price,
        "logged_user": logged_user,
        "form": form,
    }
    return render(request, "ordering_website/checkout_page.html", data)


def users(request):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    items_in_cart = get_cart_items_number(request)

    if not is_admin:
        return redirect("home")

    users = User.objects.exclude(user_uid__in=[logged_user.user_uid]).order_by('-registration_time')

    data = {
        "is_logged": is_logged,
        "is_admin": is_admin,
        "logged_user": logged_user,
        "items_in_cart": items_in_cart,
        "users": users,
    }
    return render(request, "ordering_website/users.html", data)


def remove_user(request, user_uid):
    logged_user, _ = get_user(request)
    is_admin = check_if_admin(logged_user)

    if not is_admin:
        return redirect("home")

    user_to_remove = User.objects.get(user_uid=user_uid)
    user_to_remove.delete()

    return redirect("users")


def remove_wine(request, wine_id):
    logged_user, _ = get_user(request)
    is_admin = check_if_admin(logged_user)

    if not is_admin:
        return redirect("home")

    wine_to_remove = Wine.objects.get(pk=wine_id)
    wine_to_remove.delete()

    return redirect("all_wines")


def switch_admin_user(request, user_uid):
    logged_user, _ = get_user(request)
    is_admin = check_if_admin(logged_user)

    if not is_admin:
        return redirect("home")

    chosen_user = User.objects.get(pk=user_uid)

    if chosen_user.rank == "admin":
        chosen_user.rank = "user"
    else:
        chosen_user.rank = "admin"

    chosen_user.save(update_fields=["rank"])

    return redirect("users")


def all_wines(request):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    items_in_cart = get_cart_items_number(request)

    if not is_admin:
        return redirect("home")

    wines = Wine.objects.all().order_by('-name')

    data = {
        "is_logged": is_logged,
        "is_admin": is_admin,
        "logged_user": logged_user,
        "items_in_cart": items_in_cart,
        "wines": wines,
    }
    return render(request, "ordering_website/all_wines.html", data)


def remove_opinion(request, wine_id, user_uid):
    logged_user, _ = get_user(request)
    is_admin = check_if_admin(logged_user)

    if not is_admin:
        return redirect("home")

    wine = Wine.objects.get(pk=wine_id)
    user = User.objects.get(pk=user_uid)
    opinion = Rating.objects.filter(wine=wine, author=user)
    opinion.delete()

    return redirect("wine_page", wine_id)


def orders(request):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    items_in_cart = get_cart_items_number(request)

    if not is_admin:
        return redirect("home")

    orders = OrderData.objects.all().order_by('-order_time')

    status_dict = {"ordered": "Zamówione", "paid": "Zapłacone", "sent": "Wysłane", "delivered": "Dostarczone" }

    data = {
        "is_logged": is_logged,
        "is_admin": is_admin,
        "logged_user": logged_user,
        "items_in_cart": items_in_cart,
        "orders": orders,
        "status_dict": status_dict
    }
    return render(request, "ordering_website/orders.html", data)


def check_order(request, order_id):
    logged_user, is_logged = get_user(request)
    is_admin = check_if_admin(logged_user)

    items_in_cart = get_cart_items_number(request)

    if not is_admin:
        return redirect("home")

    order = OrderData.objects.get(pk=order_id)
    ordered_wines = OrderedProduct.objects.filter(order=order_id)

    full_order_price = sum(ordered_wine.full_price for ordered_wine in ordered_wines)

    status_dict = {"ordered": "Zamówione", "paid": "Zapłacone", "sent": "Wysłane", "delivered": "Dostarczone" }

    data = {
        "is_logged": is_logged,
        "is_admin": is_admin,
        "logged_user": logged_user,
        "items_in_cart": items_in_cart,
        "order": order,
        "ordered_wines": ordered_wines,
        "full_order_price": full_order_price,
        "status_dict": status_dict
    }

    return render(request, "ordering_website/check_order.html", data)


def cancel_order(request, order_id):
    logged_user, _ = get_user(request)
    is_admin = check_if_admin(logged_user)

    if not is_admin:
        return redirect("home")

    order = OrderData.objects.get(pk=order_id)
    ordered_wines = OrderedProduct.objects.filter(order=order_id)
    for wine_order in ordered_wines:
        wine = Wine.objects.get(pk=wine_order.wine.wine_id)
        wine.in_stock += wine_order.quantity
        wine.save(update_fields=["in_stock"])

    order.delete()

    return redirect("orders")


def update_order_status(request, order_id, status):
    logged_user, _ = get_user(request)
    is_admin = check_if_admin(logged_user)

    if not is_admin:
        return redirect("home")

    order = OrderData.objects.get(pk=order_id)
    order.status = status
    order.save(update_fields=["status"])

    return redirect("check_order", order_id)

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
