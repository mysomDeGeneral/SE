from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views._login, name='login'),
    path('student-register/', views.student_register, name='student_register'),
    path('halls/', views._hall, name='halls'),
    path('hall/<int:pk>', views._rooms, name='rooms'),
    path('booking/<int:room_id>', views._booking, name='booking'),
    path('manager-home/', views.hall_manager_home, name='hall_manager_home'),
    path('logout/', views._logout_user, name='logout'),
    path('booking-details/', views._booking_details, name='booking_details'),
    path('helpdesk/', views._help, name='help'),
    path('authenticate/',views._authenticate, name='authenticate'),
    
    path('charge/', views._charge, name='charge'),
    path('cancel/', views._cancel_booking, name='cancel'),

    #test url
    path('test/', views.test, name='test'),


    #chat urls
    path('chat/', views._chat, name='chat'),
    
    path('chat/send/', views._send, name='send'),  
    path('chat/getMessages/', views._getMessages, name='getMessages')
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)