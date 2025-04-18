from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers





User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
        -This class is for adding user into database
            #- METHOD : POST 
            #- Add one user 
            #- Represent data 
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password',]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user









class LoginSerializer(serializers.Serializer):
    """
        -This class is for loging user into database
            #- METHOD : POST 
            #- validating classs
    """
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    
    class Meta :
        model = User
        fields = ['username', 'email', 'password']
    
    
    def validate(self, attrs):
        info = {}
        if 'email' in attrs :
            info['email'] = attrs['email']
        
        if 'username' in attrs :
            info['username'] = attrs['username']
            
        user = User.objects.get(**info)
        
        if user:
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError('passowrd does not match')
            attrs['id'] = user
            return attrs
        raise serializers.ValidationError('user not found')