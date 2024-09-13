from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status

from apps.user.serializers import UserLoginSerializer
from apps.taskapp.tasks import send_otp_to_number
from apps.user.models.user import User
from django.core.cache import caches
from apps.user.serializers import VerifyAccountSerializer
from apps.user.serializers import ResetOtpCustomerSerializer
from rest_framework_simplejwt.tokens import RefreshToken



class VerifyUserOtpApi(APIView):
    def post(self, request):

        serializer = VerifyAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']

        # For Testing Google Play and App Store
        if otp == '0001':
            user = User.objects.get(phone='994554708786')
            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            return Response({
                'message': 'Account verified',
                'data': data
            },
                status=200
            )

        # get cached data
        otp_cache = caches['otp-cache']
        cached_data = otp_cache.get(otp)

        if cached_data is None:
            return Response({
                'message': 'OTP code is expired',}, status=404)

        user = User.objects.filter(phone=cached_data[0]).first()

        if cached_data is None or not user:
            return Response({'result': False}, status=400)

        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return Response({
            'message': 'Account verified',
            'data': data
            },
            status=200
        )


class ResetOtp(APIView):
    def post(self, request, *args, **kwargs):

        serializer = ResetOtpCustomerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():

            send_otp_to_number.delay((serializer.data['phone']))

            return Response({
                'status': 200,
                'message': 'Reset OTP was successful, please check the phone',
                'data': serializer.data
            })

        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })


class LoginUserApi(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data.get("phone")

            user = User.objects.filter(phone=phone).first()
            if not user:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Phone",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)

            else:
                if serializer.data['phone'] != '994554708786':
                    send_otp_to_number.delay((serializer.data['phone']))

                response = {
                     "status": status.HTTP_200_OK,
                     "message": "Otp sent successfully",
                     "data": serializer.data
                     }
                return Response(response, status=status.HTTP_200_OK)

        response = {
            "status": status.HTTP_404_NOT_FOUND,
            "message": "Invalid phone number",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

