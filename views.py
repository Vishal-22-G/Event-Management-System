from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from events.models import Event
from .forms import AttendeeSignUpForm, AdminSignUpForm, AttendeeLoginForm, AdminLoginForm
from .models import CustomUser
from django.contrib import messages
from events.forms import EventRegistrationForm
from django.shortcuts import render, get_object_or_404, redirect
from events.models import  EventRegistration


def home(request):
    return render(request, 'users/home.html')

def attendee_signup(request):
    if request.method == 'POST':
        form = AttendeeSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_attendee = True
            user.save()
            login(request, user)
            return redirect('attendee_dashboard')
    else:
        form = AttendeeSignUpForm()
    return render(request, 'users/attendee_signup.html', {'form': form})

def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True
            user.save()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AdminSignUpForm()
    return render(request, 'users/admin_signup.html', {'form': form})

def attendee_login(request):
    if request.method == 'POST':
        form = AttendeeLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('attendee_dashboard')
    else:
        form = AttendeeLoginForm()
    return render(request, 'users/attendee_login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AdminLoginForm()
    return render(request, 'users/admin_login.html', {'form': form})

@login_required
def admin_dashboard(request):
    attendees = CustomUser.objects.filter(is_attendee=True)
    events = Event.objects.all()
    return render(request, 'users/admin_dashboard.html', {'attendees': attendees, 'events': events})


@login_required
def attendee_dashboard(request):
    events = Event.objects.all()
    registered_events = EventRegistration.objects.filter(attendee=request.user).select_related('event')

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            event = get_object_or_404(Event, id=event_id)

            # Check if already registered
            if registered_events.filter(event=event).exists():
                messages.warning(request, f'You are already registered for "{event.title}".')
            elif event.available_seats() > 0:
                # Register the user
                EventRegistration.objects.create(event=event, attendee=request.user)
                messages.success(request, f'Successfully registered for "{event.title}".')
            else:
                messages.error(request, f'Sorry, "{event.title}" is fully booked.')

            return redirect('attendee_dashboard')

    form = EventRegistrationForm()

    return render(request, 'users/attendee_dashboard.html', {
        'events': events,
        'registered_events': registered_events,  # Correctly fetching registered events
        'form': form
    })




def logout_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:  # Admin User
            logout(request)
            return redirect('admin_login')  # Redirect to Admin Login Page
        else:  # Attendee User
            logout(request)
            return redirect('attendee_login')  # Redirect to Attendee Login Page

    return redirect('attendee_login')  # Default Redirect (if somehow user isn't logged in)