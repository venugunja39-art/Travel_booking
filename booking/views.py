from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, BookingForm
from .models import TravelOption, Booking

# Home page → Show available travels
def home(request):
    travels = TravelOption.objects.all()

    # Filters
    travel_type = request.GET.get("type")
    source = request.GET.get("source")
    destination = request.GET.get("destination")

    if travel_type and travel_type != "All":
        travels = travels.filter(type=travel_type)
    if source:
        travels = travels.filter(source__icontains=source)
    if destination:
        travels = travels.filter(destination__icontains=destination)

    return render(request, "booking/home.html", {"travels": travels})


# Register new user
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "booking/register.html", {"form": form})

# Book a travel option
@login_required
def book_travel(request, travel_id):
    travel = get_object_or_404(TravelOption, id=travel_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.travel_option = travel
            booking.total_price = travel.price * booking.number_of_seats

            # Validation: Check seats
            if booking.number_of_seats <= travel.available_seats and booking.number_of_seats > 0:
                travel.available_seats -= booking.number_of_seats
                travel.save()
                booking.save()
                return redirect("my_bookings")
            else:
                form.add_error("number_of_seats", "Not enough seats available.")
    else:
        form = BookingForm()
    return render(request, "booking/book_travel.html", {"form": form, "travel": travel})

# My Bookings page
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "booking/my_bookings.html", {"bookings": bookings})

# Cancel booking
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == "Confirmed":
        # Restore seats
        booking.travel_option.available_seats += booking.number_of_seats
        booking.travel_option.save()
        booking.status = "Cancelled"
        booking.save()
    return redirect("my_bookings")
