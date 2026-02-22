from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from services.auth_service import AuthService
from services.email_service import EmailService
from .forms import UserRegistrationForm
from orders.models import Order
# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Call our Service (Business Logic)
            user = AuthService.register_user(email, password)
            
            # Send Email
            domain = request.get_host()
            protocol = request.scheme
            EmailService.send_activation_email(user, domain, protocol)

            messages.success(request, "Check your email to activate your account!")
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def activate_view(request, uidb64, token):
    """
    This activates the email of a person
    """

    success, message = AuthService.activate_user(uidb64, token)

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)


    return redirect('accounts:login')


def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next')

        if email and password:
            # check if the credentials are valid
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                # messages.success(request, f"Welcome back, {user.display_name}")

                if next_url and next_url != '':
                    return redirect(next_url)

                return redirect('products:product_list')
            else:
                # Authentication failed (wrong password OR is_active=False)
                messages.error(request, "Invalid email or password. Please try again.")
        else:
            messages.error(request, "Please provide both email and password.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out safely")
    return redirect("accounts:login")

@login_required(login_url='accounts:login')
def dashboard_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')


    context = {
        'orders':orders
        }
    
    return render(request, 'accounts/dashboard.html', context)