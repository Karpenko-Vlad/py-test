from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'phone_number',
            'country',
            'city',
            'street',
            'postcode'
        )

    def custom_validate(self):
        for field in self.Meta.fields:
            if field not in self.data or self.data[field] is None:
                return False, f"Field '{field}' not exist or empty"

        if User.objects.filter(username=self.data['username']).first():
            return False, "Username already exist"
        elif User.objects.filter(username=self.data['email']).first():
            return False, "Email already exist"

        return True, ''
