from rest_framework import serializers
from events.models import Category,Event
from datetime import date

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id"]

class EventSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only =True)
    #owner_name = serializers.CharField(source = "owner.username",read_only = True)
    category_name = serializers.CharField(read_only = True,source = "category.name")
    #status = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["id","owner","created_at","category_name","status"]

   