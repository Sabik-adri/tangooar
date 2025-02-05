from rest_framework import serializers
from .models import BoatOwnerProfile

class BoatOwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoatOwnerProfile
        fields = '__all__'
