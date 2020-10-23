from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'username',
                  'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(raw_password=validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    credential = serializers.CharField()
    password = serializers.CharField(min_length=6)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)