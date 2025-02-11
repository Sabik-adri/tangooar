from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('SuperAdmin', 'SuperAdmin'),
        ('Admin', 'Admin'),
        ('BoatOwner', 'BoatOwner'),
        ('Manager', 'Manager'),
        ('Customer', 'Customer'),
    ]
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=ROLES[-1][0],
    )
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users_permissions',
        blank=True
    )

class BoatOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='boat_owner_profile')
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class Boat(models.Model):
    owner_profile = models.ForeignKey(BoatOwnerProfile, on_delete=models.CASCADE, related_name='boats')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=50,
        choices=[('House boat', 'House boat'), ('Semi House boat', 'Semi House boat'), ('Traditional boat', 'Traditional boat')]
    )
    cabin_quantity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    booked_dates = models.TextField(blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    photos = models.TextField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

class Cabin(models.Model):
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, related_name='cabins')
    name = models.CharField(max_length=255)
    cabin_no = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_dates = models.TextField(blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    photos = models.TextField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    owner_profile = models.ForeignKey('boats.BoatOwnerProfile', on_delete=models.CASCADE, related_name='managers')
    name = models.CharField(max_length=255, blank=True, null=True)
    assigned_boats = models.TextField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)



class ScheduleCalendar(models.Model):
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, blank=True, null=True, related_name='schedules')
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE, blank=True, null=True, related_name='schedules')
    available_dates = models.TextField(blank=True, null=True)
    reserved_dates = models.TextField(blank=True, null=True)
    package_tour = models.TextField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_profile')
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

class Booking(models.Model):
    customer = models.ForeignKey('boats.Customer', on_delete=models.CASCADE, related_name='bookings')
    boat = models.ForeignKey('boats.Boat', on_delete=models.CASCADE, blank=True, null=True, related_name='bookings')
    cabin = models.ForeignKey('boats.Cabin', on_delete=models.CASCADE, blank=True, null=True, related_name='bookings')
    booking_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

class TourType(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

class TourPackage(models.Model):
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, related_name='packages')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_packages')
    booked_by = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='booked_packages')
    tour_type = models.ForeignKey(TourType, on_delete=models.CASCADE, related_name='packages')
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    start_from = models.CharField(max_length=255)
    destinations = models.TextField()
    guest_amount = models.IntegerField()
    guest_limitation = models.IntegerField()
    package_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cabin_quantity = models.IntegerField(blank=True, null=True)
    cabin_names = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

class TourPackageSchedule(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='schedules')
    schedule_date = models.DateField()
    schedule_time = models.TimeField()
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

