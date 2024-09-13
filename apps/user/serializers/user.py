from rest_framework import serializers
from apps.user.models.user import User
from rest_framework.exceptions import ValidationError



class VerifyAccountSerializer(serializers.Serializer):

    otp = serializers.CharField()

    def validate_otp(self, otp):
        if len(str(otp)) != 4:
            raise ValidationError('OTP must be 4-digit integer.')
        return otp


class ResetOtpCustomerSerializer(serializers.Serializer):
    phone = serializers.IntegerField(required=True)


class UserLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()

    class Meta:
        model = User
        fields = ['phone',]




