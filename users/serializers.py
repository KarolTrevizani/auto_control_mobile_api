from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes user instances, including fields: id, name, username, email, cnh, and type.
    Used primarily for read operations in user management.
    """

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email', 'cnh', 'type')


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Handles creation of new user instances. Serializes user data and enforces password to be write-only.
    Includes fields: id, email, password, name, cnh, and type. Overrides the create method to handle
    custom user creation logic, including setting the password securely.
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'cnh', 'type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
            name=validated_data['name'],
            cnh=validated_data['cnh']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Authenticates a user based on username and password. Raises validation errors separately 
    for non-existent username or incorrect password.
    """

    username = serializers.CharField(label="Username")
    password = serializers.CharField(label="Password", style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if not username:
            raise serializers.ValidationError({'username': 'Username is required.'}, code='authorization')
        
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'}, code='authorization')
        
        user = authenticate(username=username, password=password)
        if not user:
            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError({'username': 'User with this username does not exist.'}, code='authorization')
            else:
                raise serializers.ValidationError({'password': 'Password is incorrect.'}, code='authorization')

        attrs['user'] = user
        return attrs
    

class ChangePasswordSerializer(serializers.Serializer):
    """
    Allows users to change their password. Requires the old password for authentication and the new
    password to update. Ensures that password changes are securely handled.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)