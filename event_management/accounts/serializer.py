from accounts.models import CustomUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","username","password","email","phone"]
        read_only_fields = ["id"]

    def create(self,validate_data):
        return CustomUser.objects.create_user(**validate_data)


        