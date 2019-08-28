from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
# whenever you're outputting any messages in the Python code that are
# going to be out of screen it's a good idea to pass them through
# this translation
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # Serializer for the users object

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        # Create a new user with encrypted password and return it
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    # Serializer for the user authentication object
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False  # possible to have whitespace in your password
    )

    def validate(self, attrs):
        # Validate and authenticate the user
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            # we can translate it into different languages if we choose
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
        # when you're overwritting the validate function you must return values
        # at the end
