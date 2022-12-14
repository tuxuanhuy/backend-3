from django.urls import path, include

from .views import *

urlpatterns = [
    path('user/', UserList.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('user/<int:pk>/shift', UserShift.as_view(), name='user_shift_detail'),
    path('user/<int:pk>/picture', UserPicture.as_view(), name='user_picture_detail'),

    path('shift/', ShiftList.as_view(), name='shift_list'),
    path('shift/search/', ShiftSearch.as_view(), name='shift_search'),
    path('shift/today/', ShiftToday.as_view(), name='shift_today'),
    # path('shift/range/', ShiftRange.as_view(), name='shift_range'),
    path('shift/<int:pk>/', ShiftDetail.as_view(), name='shift_detail'),
    path('login/', LoginAPI.as_view()),
    path('register/', RegisterAPI.as_view()),

]
