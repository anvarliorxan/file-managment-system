from django.urls import path
from api.user.auth import LoginUserApi
from api.user.auth import VerifyUserOtpApi
from api.user.auth import ResetOtp
from api.user.file import FileUploadApi
from api.user.file import FileUpdateApi
from api.user.file import PublicFileListApi
from api.user.file import FileDownloadApi
from api.user.file import MyFileListApi
from api.user.file import SharedFileDownloadApi
from api.user.file import FileDeleteApi
from api.user.file import GetFileApi
from api.user.comment import CommentDeleteApi
from api.user.comment import CommentCreateApi


urlpatterns = [
    # User
    path('user/login', LoginUserApi.as_view()),
    path('user/verify', VerifyUserOtpApi.as_view()),
    path('user/reset-otp', ResetOtp.as_view()),
    path('user/files', MyFileListApi.as_view()),


    # File
    path('file/upload', FileUploadApi.as_view()),
    path('file/update/<str:pk>', FileUpdateApi.as_view()),
    path('file/<str:pk>', GetFileApi.as_view()),
    path('file/delete/<str:pk>', FileDeleteApi.as_view()),
    path('file/download/<str:pk>', FileDownloadApi.as_view()),
    path('file/shared/download/<str:token>/', SharedFileDownloadApi.as_view(), name='shared-file-download'),
    path('files', PublicFileListApi.as_view()),


    # Comment
    path('comment/delete/<str:pk>', CommentDeleteApi.as_view()),
    path('comment/create', CommentCreateApi.as_view()),
]
