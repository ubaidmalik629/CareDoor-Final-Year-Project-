"""
URL configuration for CareDoor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from caredoor_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('appointmentlist/', views.appointmentlist, name='Dashboard'),
    path('registerpatient/', views.registerpatient),
    path('signup/', views.signup_view),
    path('my-appointments/', views.appointments),
    path('dctor-page2/', views.listdoctors),
    path('dctor-form/', views.registerdoctor),
    path('recep-page2/', views.listreceptionist),
    path('recep-form/', views.registerreceptionist),
    path('patient-form/', views.listpatient),
    path('treatments/', views.treatments),
    path('patient_profile/', views.patient_profile),
    path('doctor_profile/', views.doctor_profile),
    path('receptionist_profile/', views.receptionist_profile),
    path('textbox/', views.textbox),
    path('check-availability/<int:doctor_id>/', views.check_availability),
    path('inbox-page/', views.inbox_page),
    path('categories/', views.categories),
    path('list-of-doctors/<int:category_id>/', views.listofdoctors),
    path('book-slot/<int:doctor_id>/<str:start_time>/', views.book_slot),
    path('messages/<int:receiver_id>/', views.message),
    path('get_messages/<int:receiver_id>/', views.get_message),
    path('mytreatments/', views.mytreatments),
    path('my-appointments/<int:appointment_id>/cancel/', views.cancel),
    path('patient-prescription/', views.patient_prescription),
    path('patient-prescription-page/<int:prescription_id>/', views.patient_prescription_page, name='prescription-name'),
    path('doctor-prescription/', views.doctor_prescription),
    path('doctor-prescription-page/<int:prescription_id>/', views.doctor_prescription_page),
    path('update-doctor/<int:doctor_id>/', views.update_doctor),
    path('update-receptionist/<int:receptionist_id>/', views.update_receptionist),
    path('my-appointments/<int:appointment_id>/done/', views.done, name='done'),
    path('latest-prescription/<int:patient_id>/<int:doctor_id>/', views.latest_prescription),
    path('cashflow/', views.cashflow, name='cashflow'),








    path('logout/', auth_views.LogoutView.as_view(), name='logout'),



    
] + static(settings.STATIC_URL)
