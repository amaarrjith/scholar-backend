from rest_framework import serializers
from guest.models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
        
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = districts
        fields = '__all__'
        
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = states
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'
        
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = staff
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = login
        fields = '__all__'       
       
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = '__all__'  
        
class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = events
        fields = '__all__'        
        
class EventsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = eventregister
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'
        
class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = '__all__'