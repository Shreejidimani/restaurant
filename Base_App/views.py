from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
import re
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse 
from Base_App.models import BookTable, AboutUs, Feedback, ItemList, Items, Order, Category
from django.core.paginator import Paginator
from django import forms
from django.contrib.auth.models import User

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

def HomeView(request):
    items = Items.objects.all()
    item_list = ItemList.objects.all()
    reviews = Feedback.objects.all()

    # Pagination for items
    paginator = Paginator(items, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    items_page = paginator.get_page(page_number)

    context = {
        'items': items_page,
        'item_list': item_list,
        'reviews': reviews,
        'user': request.user if request.user.is_authenticated else None
    }

    return render(request, 'home.html', context)

def AboutView(request):
    data = AboutUs.objects.all()
    return render(request, 'about.html', {'data': data})

def MenuView(request):
    items = Items.objects.all()  # Fetch all items
    item_categories = Category.objects.all()  # Fetch all categories
    return render(request, 'menu.html', {
        'items': items,
        'item_categories': item_categories
    })

def menu_category(request, category_id):
    category = get_object_or_404(ItemList, id=category_id)  # Get category based on id
    items = Items.objects.filter(Category=category)  # Filter items by selected category
    return render(request, 'menu.html', {'items': items, 'selected_category': category})

def BookTableView(request):
    if request.method == 'POST':
        name = request.POST.get('user_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('user_email', '').strip()
        total_person = request.POST.get('total_person', '0').strip()
        booking_date = request.POST.get('booking_data', '').strip()

        try:
            total_person = int(total_person)
        except ValueError:
            total_person = 0

        if name and phone_number.isdigit() and len(phone_number) == 10 and email and total_person > 0 and booking_date:
            data = BookTable(
                name=name,
                phone_number=phone_number,
                email=email,
                total_person=total_person,
                booking_date=booking_date
            )
            data.save()
            messages.success(request, "Table booked successfully!")
            return redirect('Book_Table')
        else:
            messages.error(request, "Please fill all fields correctly.")
    return render(request, 'book_table.html')


def OrderView(request, item_id):
    item = get_object_or_404(Items, id=item_id)
    price_per_item = item.Price

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity', '0')
        payment_option = request.POST.get('payment_option')

        if user_name and user_email and address and quantity.isdigit() and int(quantity) > 0 and payment_option:
            total_price = price_per_item * int(quantity)

            order = Order.objects.create(
                item=item,
                user_name=user_name,
                user_email=user_email,
                address=address,
                quantity=int(quantity),
                payment_option=payment_option,
                total_price=total_price
            )

            if payment_option == 'upi':
                return redirect(reverse('upi_payment_page', kwargs={'order_id': order.id}))
            else:
                messages.success(request, "Order placed successfully!")
                return redirect(reverse('order_confirmation', kwargs={'order_id': order.id}))

        else:
            messages.error(request, "Please fill all fields correctly.")

    return render(request, 'order_form.html', {'item': item, 'price_per_item': price_per_item})


def OrderConfirmationView(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})


UPI_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$'

def upi_payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        upi_id = request.POST.get('upi_id')

        if re.match(UPI_REGEX, upi_id):
            order.upi_id = upi_id
            order.status = 'Paid'
            order.save()
            return redirect(reverse('order_confirmation', kwargs={'order_id': order.id}))
        else:
            messages.error(request, "Invalid UPI ID. Please enter a valid UPI ID.")
            return render(request, 'upi_payment.html', {'order': order})

    return render(request, 'upi_payment.html', {'order': order})


def mock_payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        upi_id = request.POST.get('upi_id')

        if not re.match(UPI_REGEX, upi_id):
            messages.error(request, "Invalid UPI ID format. Please enter a valid UPI ID.")
            return render(request, 'upi_payment.html', {'order': order})

        order.upi_id = upi_id
        order.status = 'Paid'
        order.save()

        messages.success(request, f"Payment confirmed for Order #{order.id}.")
        return redirect(reverse('order_confirmation', kwargs={'order_id': order.id}))

    return render(request, 'upi_payment.html', {'order': order})


def order_status_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_status.html', {'order': order})


def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)
    
    if status in dict(Order.STATUS_CHOICES):
        order.status = status
        order.save()
        return HttpResponse(f"Order status updated to '{status}' for Order ID {order.id}")
    else:
        return HttpResponse("Invalid status.", status=400)
    

def FeedbackView(request):
    reviews = Feedback.objects.all()  # Fetch all feedback from the database
    return render(request, 'feedback.html', {'review': reviews})

def submit_feedback(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        description = request.POST['Description']
        rating = request.POST['total_person']
        image = request.FILES['image']  # Get the uploaded image

        # Save the feedback to the database
        feedback = Feedback(User_name=user_name, Description=description, Rating=rating, Image=image)
        feedback.save()

        return redirect('home')  # Redirect to the home page or a thank you page

    return render(request, 'feedback.html') # Redirect to the home page or a thank you page

    return render(request, 'feedback.html')
@login_required
def user_profile(request):
    return render(request, 'user_profile.html', {'user': request.user})

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")  # Redirect to login page after registration
        else:
            messages.error(request, "Invalid registration details. Please try again.")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    form = AuthenticationForm()

    if request.method == "POST":
        username_or_email = request.POST.get("email_or_username")  # Get the value from the form
        password = request.POST.get("password")
        
        user = None

        # Check if it's an email or username
        if re.match(r"[^@]+@[^@]+\.[^@]+", username_or_email):  # If it's an email
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
        else:  # If it's a username
            user = authenticate(request, username=username_or_email, password=password)

        # Authenticate the user
        if user and user.check_password(password):
            login(request, user)
            return redirect("Home")  # Redirect to the home page after login
        else:
            messages.error(request, "Invalid username/email or password.")

    return render(request, "registration/login.html", {"form": form})

