from datetime import datetime, timezone
import re
from django.forms import ValidationError
from django.shortcuts import render

from .form import BoatForm

from .models import Manager
from .models import BoatOwnerProfile, Boat, Cabin, ScheduleCalendar, Customer, Booking, TourType, TourPackage, TourPackageSchedule
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
import json
from .models import BoatOwnerProfile
from django.contrib.auth.hashers import make_password
from .models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone


# Hi I am Adri

def dashboard_view(request):
    boats = Boat.objects.all()
    context = {
        'boats': boats
    }
    return render(request, 'index.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to a dashboard or homepage after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'boats/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to a dashboard or homepage after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'boats/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')



# User
def user_create_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        password = make_password(request.POST.get("password"))  # Hash password
        phone_number = request.POST.get("phone_number")
        role = request.POST.get("role")
        
        User.objects.create(
            name=name,
            username=username,
            password=password,
            phone_number=phone_number,
            role=role,
            created_by=request.user.id if request.user.is_authenticated else None,
        )
        return redirect('create_boat_owner_profile')
    return render(request, 'boats/user_create.html')


def user_update_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.name = request.POST.get("name")
        user.username = request.POST.get("username")
        if request.POST.get("password"):  # Optional password change
            user.password = make_password(request.POST.get("password"))
        user.phone_number = request.POST.get("phone_number")
        user.role = request.POST.get("role")
        user.updated_by = request.user.id if request.user.is_authenticated else None
        user.save()
        return redirect('create_boat_owner_profile')
    return render(request, 'boats/user_update.html', {'user': user})


def user_delete_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.deleted_by = request.user.id if request.user.is_authenticated else None
        user.deleted_at = timezone.now()
        user.save()  # Soft delete (optional)
        # For hard delete: user.delete()
        return redirect('create_boat_owner_profile')
    return render(request, 'boats/user_delete.html', {'user': user})


# Boat Owner Profile
@csrf_exempt
def create_boat_owner_profile_view(request):
    if request.method == "POST":
        form_data = request.POST
        user_id = form_data.get("user")
        user = get_object_or_404(User, id=user_id)
        
        BoatOwnerProfile.objects.create(
            user=user,
            company_name=form_data.get("company_name"),
            address=form_data.get("address"),
            contact_number=form_data.get("contact_number"),
            email=form_data.get("email"),
        )
        return redirect('boat_owner_profiles')
    
    # Pass all users to the template for the dropdown
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'boats/boat_owner_profile_create.html', context)

@csrf_exempt
def update_boat_owner_profile_view(request, pk):
    profile = BoatOwnerProfile.objects.get(pk=pk)
    if request.method == "POST":
        profile.company_name = request.POST.get("company_name")
        profile.address = request.POST.get("address")
        profile.contact_number = request.POST.get("contact_number")
        profile.email = request.POST.get("email")
        profile.save()
        return redirect('boat_owner_profiles')
    return render(request, 'boats/boat_owner_profile_update.html', {'profile': profile})

@csrf_exempt
def delete_boat_owner_profile_view(request, pk):
    profile = BoatOwnerProfile.objects.get(pk=pk)
    if request.method == "POST":
        profile.delete()
        return redirect('boat_owner_profiles')
    return render(request, 'boats/boat_owner_profile_delete.html', {'profile': profile})

def boat_owner_profile_list_view(request):
    profiles = BoatOwnerProfile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'boats/boat_owner_profile_list.html', context)





# Manager
@csrf_exempt
def create_manager_view(request):
    if request.method == "POST":
        form_data = request.POST
        user_id = form_data.get("user")
        owner_profile_id = form_data.get("owner_profile")
        
        user = get_object_or_404(User, id=user_id)
        owner_profile = get_object_or_404(BoatOwnerProfile, id=owner_profile_id)
        
        Manager.objects.create(
            user=user,
            owner_profile=owner_profile,
            name=form_data.get("name"),
            assigned_boats=form_data.get("assigned_boats"),
            created_by=request.user.id,
        )
        return redirect('manager_list')
    
    users = User.objects.all()
    owner_profiles = BoatOwnerProfile.objects.all()
    context = {
        'users': users,
        'owner_profiles': owner_profiles,
    }
    return render(request, 'boats/manager_create.html', context)

@csrf_exempt
def update_manager_view(request, pk):
    manager = get_object_or_404(Manager, pk=pk)
    if request.method == "POST":
        manager.user = get_object_or_404(User, id=request.POST.get("user"))
        manager.owner_profile = get_object_or_404(BoatOwnerProfile, id=request.POST.get("owner_profile"))
        manager.name = request.POST.get("name")
        manager.assigned_boats = request.POST.get("assigned_boats")
        manager.updated_by = request.user.id
        manager.save()
        return redirect('manager_list')
    
    users = User.objects.all()
    owner_profiles = BoatOwnerProfile.objects.all()
    context = {
        'manager': manager,
        'users': users,
        'owner_profiles': owner_profiles,
    }
    return render(request, 'boats/manager_update.html', context)

@csrf_exempt
def delete_manager_view(request, pk):
    manager = get_object_or_404(Manager, pk=pk)
    if request.method == "POST":
        manager.deleted_by = request.user.id
        manager.deleted_at = timezone.now()
        manager.save()  # Soft delete, if you want to retain the record
        # manager.delete() # Uncomment this for hard delete
        return redirect('manager_list')
    context = {
        'manager': manager
    }
    return render(request, 'boats/manager_delete.html', context)

def manager_list_view(request):
    managers = Manager.objects.all()
    context = {
        'managers': managers
    }
    return render(request, 'boats/manager_list.html', context)





# Customer
@csrf_exempt
def create_customer_view(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        user = get_object_or_404(User, id=user_id)
        Customer.objects.create(
            user=user,
            created_by=request.user.id
        )
        return redirect('customer_list')
    
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'boats/customer_create.html', context)

@csrf_exempt
def update_customer_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.user = get_object_or_404(User, id=request.POST.get("user"))
        customer.updated_by = request.user.id
        customer.save()
        return redirect('customer_list')
    
    users = User.objects.all()
    context = {
        'customer': customer,
        'users': users
    }
    return render(request, 'boats/customer_update.html', context)

@csrf_exempt
def delete_customer_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.deleted_by = request.user.id
        customer.deleted_at = timezone.now()
        customer.save()  # For soft delete
        # customer.delete() # Uncomment for hard delete
        return redirect('customer_list')
    return render(request, 'boats/customer_delete.html', {'customer': customer})

def customer_list_view(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'boats/customer_list.html', context)



# Boat
def boat_list_view(request):
    boats = Boat.objects.all()
    context = {
        'boats': boats
    }
    return render(request, 'transports-list.html', context)

def boat_list_view_index(request):
    boats = Boat.objects.all()
    context = {
        'boats': boats
    }
    return render(request, 'index.html', context)

def get_boat_details(request, boat_id):
    try:
        boat = Boat.objects.prefetch_related('cabins', 'schedules').get(id=boat_id)

        # Get schedule info (assuming boat-based schedules)
        schedule = boat.schedules.first()
        available_dates = schedule.available_dates.split(',') if schedule and schedule.available_dates else []
        reserved_dates = schedule.reserved_dates.split(',') if schedule and schedule.reserved_dates else []
        calendar_days = list(range(1, 31))  # [1, 2, ..., 30]

        data = {
            'id': boat.id,
            'name': boat.name,
            'description': boat.description,
            'price': boat.price,
            'type': boat.type,
            'cabin_quantity': boat.cabin_quantity,
            'is_reserved': boat.is_reserved,
            'length': boat.length,
            'width': boat.width,
            'height': boat.height,
            'photos': request.build_absolute_uri(boat.photos.url) if boat.photos else '',
            'owner_profile': {
                'company_name': boat.owner_profile.company_name
            },
            'cabins': boat.cabins.all(),
            'available_dates': available_dates,
            'reserved_dates': reserved_dates,
            'booked_dates' : boat.booked_dates,
            'calendar_days': calendar_days  # Add the list of days to the context
        }

        return render(request, 'booking-sheet.html', {'boat': data})
    except Boat.DoesNotExist:
        return render(request, 'booking-sheet.html', {'error': 'Boat not found'})

@csrf_exempt
def create_boat_view(request):
    if request.method == "POST":
        owner_id = request.POST.get("owner_profile")
        owner_profile = get_object_or_404(BoatOwnerProfile, id=owner_id)
        
        # Validate booked_dates format (e.g., "2025-05-01:2025-05-05,2025-06-01:2025-06-07")
        booked_dates = request.POST.get("booked_dates")
        if booked_dates:
            try:
                # Simple validation: check if dates match YYYY-MM-DD:YYYY-MM-DD format
                date_ranges = booked_dates.split(",")
                date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}$")
                for date_range in date_ranges:
                    if not date_pattern.match(date_range):
                        raise ValidationError(f"Invalid date range format: {date_range}")
                    start_date, end_date = date_range.split(":")
                    # Optionally, validate that dates are valid and start_date <= end_date
                    from datetime import datetime
                    start = datetime.strptime(start_date, "%Y-%m-%d")
                    end = datetime.strptime(end_date, "%Y-%m-%d")
                    if start > end:
                        raise ValidationError(f"Start date must be before end date in range: {date_range}")
            except ValidationError as e:
                return render(request, 'boats/boat_create.html', {
                    'owners': BoatOwnerProfile.objects.all(),
                    'error': str(e)
                })

        boat = Boat.objects.create(
            owner_profile=owner_profile,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            type=request.POST.get("type"),
            cabin_quantity=request.POST.get("cabin_quantity"),
            length=request.POST.get("length"),
            width=request.POST.get("width"),
            height=request.POST.get("height"),
            created_by=request.user.id,
            photos=request.FILES.get("photos")
        )
        return redirect('boat_list')

    owners = BoatOwnerProfile.objects.all()
    return render(request, 'boats/boat_create.html', {'owners': owners})

@csrf_exempt
def update_boat_view(request, pk):
    boat = get_object_or_404(Boat, pk=pk)
    if request.method == "POST":
        form = BoatForm(request.POST, request.FILES, instance=boat)
        if form.is_valid():
            form.instance.updated_by = request.user.id
            form.save()
            return redirect('boat_list')
        context = {
            'boat': boat,
            'owners': BoatOwnerProfile.objects.all(),
            'form': form
        }
        return render(request, 'boats/boat_update.html', context)
    form = BoatForm(instance=boat)
    context = {
        'boat': boat,
        'owners': BoatOwnerProfile.objects.all(),
        'form': form
    }
    return render(request, 'boats/boat_update.html', context)

@csrf_exempt
def delete_boat_view(request, pk):
    boat = get_object_or_404(Boat, pk=pk)
    if request.method == "POST":
        boat.deleted_by = request.user.id
        boat.deleted_at = timezone.now()
        boat.save()  # For soft delete
        # boat.delete()  # Uncomment for hard delete
        return redirect('boat_list')
    return render(request, 'boats/boat_delete.html', {'boat': boat})


# Cabin
# def cabin_list_view(request):
#     cabins = Cabin.objects.all()
#     context = {
#         'cabins': cabins
#     }
#     return render(request, 'boats/cabin_list.html', context)

def cabin_list_view(request):
    boats = Boat.objects.prefetch_related('cabins').all()
    context = {'boats': boats}
    return render(request, 'boats/cabin_list.html', context)


def get_cabin_details(request, cabin_id):
    try:
        cabin = Cabin.objects.get(id=cabin_id)
        data = {
            'id': cabin.id,
            'name': cabin.name,
            'cabin_no': cabin.cabin_no,
            'description': cabin.description,
            'price': str(cabin.price),
            'length': str(cabin.length) if cabin.length else None,
            'width': str(cabin.width) if cabin.width else None,
            'height': str(cabin.height) if cabin.height else None,
            'photos': cabin.photos,
            'created_at': cabin.created_at.isoformat(),
        }
        return JsonResponse(data)
    except Cabin.DoesNotExist:
        return JsonResponse({'error': 'Cabin not found'}, status=404)


@csrf_exempt
def create_cabin_view(request):
    if request.method == "POST":
        boat_id = request.POST.get("boat")
        boat = get_object_or_404(Boat, id=boat_id)
        Cabin.objects.create(
            boat=boat,
            name=request.POST.get("name"),
            cabin_no=request.POST.get("cabin_no"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            length=request.POST.get("length"),
            width=request.POST.get("width"),
            height=request.POST.get("height"),
            created_by=request.user.id
        )
        return redirect('cabins')

    boats = Boat.objects.all()
    context = {'boats': boats}
    return render(request, 'boats/cabin_create.html', context)

@csrf_exempt
def update_cabin_view(request, pk):
    cabin = get_object_or_404(Cabin, pk=pk)
    if request.method == "POST":
        cabin.boat = get_object_or_404(Boat, id=request.POST.get("boat"))
        cabin.name = request.POST.get("name")
        cabin.cabin_no = request.POST.get("cabin_no")
        cabin.description = request.POST.get("description")
        cabin.price = request.POST.get("price")
        cabin.length = request.POST.get("length")
        cabin.width = request.POST.get("width")
        cabin.height = request.POST.get("height")
        cabin.updated_by = request.user.id
        cabin.save()
        return redirect('cabins')

    boats = Boat.objects.all()
    context = {'cabin': cabin, 'boats': boats}
    return render(request, 'boats/cabin_update.html', context)

@csrf_exempt
def delete_cabin_view(request, pk):
    cabin = get_object_or_404(Cabin, pk=pk)
    if request.method == "POST":
        cabin.deleted_by = request.user.id
        cabin.deleted_at = timezone.now()
        cabin.save()  # Soft delete
        cabin.delete()
        return redirect('cabins')

    return render(request, 'boats/cabin_delete.html', {'cabin': cabin})

def schedule_calendar_list_view(request):
    schedules = ScheduleCalendar.objects.all()
    context = {
        'schedules': schedules
    }
    return render(request, 'boats/schedule_calendar_list.html', context)



def booking_list_view(request):
    bookings = Booking.objects.all()
    context = {
        'bookings': bookings
    }
    return render(request, 'boats/booking_list.html', context)

def tour_type_list_view(request):
    tour_types = TourType.objects.all()
    context = {
        'tour_types': tour_types
    }
    return render(request, 'boats/tour_type_list.html', context)

def tour_package_list_view(request):
    packages = TourPackage.objects.all()
    context = {
        'packages': packages
    }
    return render(request, 'boats/tour_package_list.html', context)

def tour_package_schedule_list_view(request):
    schedules = TourPackageSchedule.objects.all()
    context = {
        'schedules': schedules
    }
    return render(request, 'boats/tour_package_schedule_list.html', context)

# @csrf_exempt
# def book_date(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         boat_id = data.get('boat_id')
#         date = data.get('date')

#         schedules = ScheduleCalendar.objects.filter(boat_id=boat_id)
#         if schedules.exists():
#             schedule = schedules.first()  # Take the first schedule
#             reserved = [d.strip() for d in schedule.reserved_dates.split(',')] if schedule.reserved_dates else []
#             available = [d.strip() for d in schedule.available_dates.split(',')] if schedule.available_dates else []

#             if date in available and date not in reserved:
#                 reserved.append(date)
#                 schedule.reserved_dates = ','.join(reserved)
#                 schedule.available_dates = ','.join([d for d in available if d != date])
#                 schedule.save()
#                 return JsonResponse({'status': 'success'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Date not available or already booked'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Schedule not found'})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# def calendar_data(request, boat_id):
#     schedules = ScheduleCalendar.objects.filter(boat_id=boat_id)
#     if schedules.exists():
#         schedule = schedules.first()  # Take the first schedule
#         available = [d.strip() for d in schedule.available_dates.split(',')] if schedule.available_dates else []
#         reserved = [d.strip() for d in schedule.reserved_dates.split(',')] if schedule.reserved_dates else []
#         return JsonResponse({
#             'status': 'success',
#             'available_dates': available,
#             'reserved_dates': reserved,
#         })
#     else:
#         return JsonResponse({'status': 'success', 'available_dates': [], 'reserved_dates': []})
    
    
def get_boat_cabins(request, boat_id):
    try:
        boat = Boat.objects.get(id=boat_id)
        cabins = boat.cabins.all()
        cabin_list = []
        for cabin in cabins:
            cabin_list.append({
                'id': cabin.id,
                'name': cabin.name,
                'cabin_no': cabin.cabin_no,
                'description': cabin.description,
                'price': float(cabin.price),
                'booked': bool(cabin.booked_dates),  # Adjust logic as needed
            })

        return JsonResponse({
            'status': 'success',
            'boat': {
                'id': boat.id,
                'name': boat.name,
                'price': float(boat.price),
                'cabin_quantity': boat.cabin_quantity
            },
            'cabins': cabin_list
        })
    except Boat.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Boat not found'}, status=404)
    
def payment_gateway(request):
    return render(request, 'payment-gateway.html')
