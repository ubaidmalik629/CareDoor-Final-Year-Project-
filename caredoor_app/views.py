from datetime import datetime, timedelta, time
import logging
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from .models import User, Appointment, Messages, Categories, Prescription, Cashflow
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils import timezone

def is_admin(user):
    return user.user_type == "A"

def is_doctor(user):
    return user.user_type == "D"

def is_receptionist(user):
    return user.user_type == "R"

def is_patient(user):
    return user.user_type == "P"

logger = logging.getLogger("hms")

# Appointment interval in Minutes
APPOINTMENT_INTERVAL = 30


User = get_user_model()
def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use a different email.")
        elif User.objects.filter(contact=contact).exists():
            messages.error(request, "Contact number already registered. Please use a different contact number.")
        else:
            first_name = request.POST.get("f_name")
            last_name = request.POST.get("l_name")
            user_data = {
                "name": f"{first_name} {last_name}",
                "contact": contact,
                "age": request.POST.get("age"),
                "email": email,
                "gender": request.POST.get("gender")[0].upper(),
                "address": request.POST.get("address"),
                "user_type": "P",
            }
            patient = User(**user_data)
            patient.set_password(request.POST.get("password"))
            patient.save()
            messages.success(request, "Signup Successful!")
            return redirect("../")
    
    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        logger.info(f"user data, {request.POST}")
        if user is not None:
            login(request, user)
            logger.info("I am here!")

            if user.user_type == "A":
                return redirect("dctor-page2/")
            elif user.user_type == "D":
                return redirect("doctor_profile/")
            elif user.user_type == "P":
                return redirect("patient_profile/")
            else:
                return redirect("receptionist_profile/")
        else:
            messages.error(request, "Access denied. Incorrect email or password.")
            return render(request, "login.html")
            
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url='/')
@user_passes_test(is_admin, login_url='/')

def update_receptionist(request, receptionist_id):
    receptionist = User.objects.filter(id=receptionist_id).first()

    if request.method == 'POST':
        if not receptionist.password == request.POST["password"]:
            receptionist.set_password(request.POST["password"])
            print('Password updated!')
        
        receptionist.name = request.POST.get("f_name") + " " + request.POST.get("l_name")
        receptionist.email = request.POST.get("email")
        receptionist.age = int(request.POST.get("age", 33))
        receptionist.contact = request.POST.get("contact", 87123871263)
        receptionist.gender = request.POST.get("gender", "O")[0].upper()
        receptionist.address = request.POST.get("address")
        receptionist.user_type = "R"

        receptionist.save()

        return redirect("/recep-page2/")
    
    name = receptionist.name.split()
    receptionist.first_name = name[0]
    receptionist.last_name = name[1]

    return render(request, "admin/update-receptionist.html", {"receptionist": receptionist})

@login_required(login_url='/')
@user_passes_test(is_admin, login_url='/')

def update_doctor(request, doctor_id):
    doctor = User.objects.filter(id=doctor_id).first()

    if request.method == 'POST':
        if not doctor.password == request.POST["password"]:
            doctor.set_password(request.POST["password"])
            print('Password updated!')
        
        doctor.name = request.POST.get("f_name") + " " + request.POST.get("l_name")
        doctor.email = request.POST.get("email")
        doctor.age = int(request.POST.get("age", 33))
        doctor.contact = request.POST.get("contact", 87123871263)
        doctor.address = request.POST.get("address", "hospital")
        doctor.gender = request.POST.get("gender", "O")[0].upper()
        doctor.user_type = "D"
        doctor.specialization_id = request.POST.get("specialization")
        doctor.check_in = request.POST.get('checkin')
        doctor.check_out = request.POST.get('checkout')
        doctor.weekdays = request.POST.getlist('weekdays')        

        doctor.save()

        return redirect("/dctor-page2/")
    
    name = doctor.name.split()
    doctor.first_name = name[0]
    doctor.last_name = name[1]
    categories = Categories.objects.all()

    return render(request, "admin/update-doctor.html", {"doctor": doctor, "categories": categories})

@login_required(login_url='/')
@user_passes_test(is_admin, login_url='/')

def listpatient(request):
    patient = User.objects.filter(user_type="P")
    print("patient", patient)
    return render(request, "admin/patient-form.html", {"patient": patient})

@login_required(login_url='/')
@user_passes_test(is_receptionist, login_url='/')

def registerpatient(request):
    if request.method == "POST":
        user = User(
            name=request.POST.get("f_name") + " " + request.POST.get("l_name"),
            email=request.POST["email"],
            age=int(request.POST["age"]),
            contact=request.POST["contact"],
            address=request.POST.get("address", ""),
            gender=request.POST["gender"][0].upper(),
            user_type="P",
        )
        user.set_password(request.POST["password"])
        user.save()
        return redirect("../appointmentlist/")
    return render(request, "registerpatient.html")

@login_required(login_url='/')
@user_passes_test(is_admin, login_url='/')

def listdoctors(request):
    doctors = User.objects.filter(user_type="D")
    print("doctors", doctors)
    return render(request, "admin/dctor-page2.html", {"doctors": doctors})

@login_required(login_url='/')
@user_passes_test(is_admin, login_url='/')

def registerdoctor(request):
    if request.method == "POST":
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use a different email.")
        elif User.objects.filter(contact=contact).exists():
            messages.error(request, "Contact number already registered. Please use a different contact number.")
        else:
            user_data = {
                "name": f"{request.POST.get('f_name')} {request.POST.get('l_name')}",
                "email": email,
                "age": int(request.POST.get("age", 33)),
                "contact": contact,
                "address": request.POST.get("address", "hospital"),
                "gender": request.POST.get("gender", "O")[0].upper(),
                "user_type": "D",
                "specialization_id": request.POST.get("specialization"),
                "check_in": request.POST.get('checkin'),
                "check_out": request.POST.get('checkout'),
                "weekdays": request.POST.getlist('weekdays'),
            }
            user = User(**user_data)
            user.set_password(request.POST["password"])
            user.save()
            return redirect("../dctor-page2/")

    categories = Categories.objects.all()
    return render(request, "admin/dctor-form.html", {"categories": categories})

    # Users-profiles

@login_required(login_url='/')
@user_passes_test(is_patient, login_url='/')

def patient_profile(request):
    request.user
    patient_profile = User.objects.filter(id=request.user.id, user_type="P")
    print("patient", patient_profile)
    print(request.user.id)
    return render(
        request, "patient/patient_profile.html", {"patient": patient_profile}
    )

@login_required(login_url='/')
@user_passes_test(is_doctor, login_url='/')

def doctor_profile(request):
    request.user
    doctor_profile = User.objects.filter(id=request.user.id, user_type="D")
    print("doctor", doctor_profile)
    print(request.user.id)
    return render(
        request, "doctor/doctor_profile.html", {"doctor": doctor_profile}
    )

@login_required(login_url='/')
@user_passes_test(is_receptionist, login_url='/')

def receptionist_profile(request):
    request.user
    receptionist_profile = User.objects.filter(
        id=request.user.id, user_type="R"
    )
    print("receptionist", receptionist_profile)
    print(request.user.id)
    return render(
        request,
        "receptionist-profile.html",
        {"receptionist": receptionist_profile},
    )

@login_required(login_url='/')
@user_passes_test(is_admin, login_url='/')

def listreceptionist(request):
    receptionist = User.objects.filter(user_type="R")
    print("receptionist", receptionist)
    return render(
        request, "admin/recep-page2.html", {"receptionist": receptionist}
    )

@login_required(login_url='/')
@user_passes_test(is_admin, login_url='/')

def registerreceptionist(request):
    if request.method == "POST":
        user = User(
            name=request.POST.get("f_name") + " " + request.POST.get("l_name"),
            email=request.POST["email"],
            age=int(request.POST["age"]),
            contact=request.POST["contact"],
            address=request.POST.get("address", ""),
            gender=request.POST["gender"][0].upper(),
            user_type="R",
        )
        user.set_password(request.POST["password"])
        user.save()
        return redirect("../recep-page2/")
    return render(request, "admin/recep-form.html")



@login_required(login_url='/')
@user_passes_test(is_doctor, login_url='/')

def appointments(request):
    doctorid = request.user.id
    myappointments = Appointment.objects.prefetch_related('patient').filter(doctor_id=doctorid, status=True)
    return render(request, "doctor/my-appointments.html", {'appointments': myappointments})

def cancel(request, appointment_id):
    
    Appointment.objects.filter(id=appointment_id).delete()
    return redirect(resolve_url(appointments))

def done(request, appointment_id):
    print("Inside the done view")
    appointment = Appointment.objects.get(id=appointment_id)
    category = Categories.objects.get(id=appointment.doctor.specialization_id)
    fee = category.fee

    # Create a Cashflow entry with the current datetime
    cashflow_entry = Cashflow(
        appointment_datetime=timezone.now(),
        patient=appointment.patient.name,
        doctor=appointment.doctor.name,
        charges=fee
    )
    cashflow_entry.save()

    # Update the appointment status
    appointment.status = False
    appointment.save()
    return redirect(resolve_url(appointments))

@login_required(login_url='/')
@user_passes_test(is_doctor, login_url='/')

def treatments(request):
    return render(request, "doctor/treatments.html")

@login_required(login_url='/')
@user_passes_test(is_receptionist, login_url='/')

def appointmentlist(request):
    # Retrieve all appointments from the database
    appointments = Appointment.objects.all()

    # Prepare data to pass to the template
    appointment_data = []
    for appointment in appointments:
        data = {
            "id": appointment.id,
            "patient_id": appointment.patient.id,
            "name": appointment.patient.name,
            "doctor": appointment.doctor.name,
            "start_time": appointment.start_time,
            "fee": appointment.doctor.specialization.fee
        }
        appointment_data.append(data)

    # Render the template with the data
    return render(request, 'appointmentlist.html', {'appointments': appointment_data})

@login_required(login_url='/')
def latest_prescription(request, doctor_id, patient_id):
    latest = Appointment.objects.filter(doctor_id=doctor_id, patient_id=patient_id).order_by('-start_time').first()
    return redirect('/doctor-prescription-page/' + str(latest.id) + '/')

@login_required(login_url='/')
@user_passes_test(is_doctor, login_url='/')

def textbox(request):
    user = User.objects.filter(id=request.user.id).first()
    app_list = Appointment.objects.filter(doctor_id=request.user.id).values('patient_id')

    users = User.objects.filter(id__in=app_list).values('id', 'name')

    return render(request, "doctor/text-box.html", {'patients': users})

@login_required(login_url='/')
@user_passes_test(is_patient, login_url='/')

def available_slots(request):
    return render(request, "patient/available-slots.html")

@login_required(login_url='/')
def book_slot(request, doctor_id, start_time):
    appointment = Appointment(
        start_time=start_time, patient_id=request.user.id, doctor_id=doctor_id
    )
    appointment.save()
    return redirect(f"/check-availability/{doctor_id}/")

@login_required(login_url='/')
def check_availability(request, doctor_id):
    doctor = User.objects.filter(id=doctor_id).first()

    # Get the current date and time
    now = datetime.now()
    working_days = []
    for working_day in doctor.weekdays:
        # Find the next working day from today
        days_until_next_monday = (working_day - now.weekday() + 7) % 7
        next_working_day = now + timedelta(days=days_until_next_monday)
        working_days.append(next_working_day)

    # Calculate the time slots from check-in to check-out with provided interval
    time_slot_duration = timedelta(minutes=APPOINTMENT_INTERVAL)
    # current_time = time(
    #     *divmod((now.hour * 60 + now.minute + 60), 60)[:2]
    # )  # Round to the nearest hour
    check_in_time = doctor.check_in or time(
        9, 0
    )  # Default check-in time to 9 AM if not set
    check_out_time = doctor.check_out or time(
        14, 0
    )  # Default check-out time to 2 PM if not set

    available_slots = []
    for date in working_days:
        # Combine the date with the calculated check-in time
        start_datetime = datetime.combine(date, check_in_time)

        # Iterate through the available time slots until the check-out time
        while start_datetime.time() < check_out_time:
            free=True
            end_datetime = start_datetime + time_slot_duration
            if end_datetime.time() <= check_out_time:
                if Appointment.objects.filter(

                    doctor_id=doctor.id,
                    start_time=start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                ).exists():
                    free=False
                
                available_slots.append(
                    {
                        "start_time": start_datetime.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "end_time": end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        "free":free
                    }
                )
            start_datetime += time_slot_duration

    return render(request, "patient/check-availability.html",{"doctor": doctor, "slots": available_slots},
    )

@login_required(login_url='/')
def message(request, receiver_id):
    is_doctor = request.user.user_type == 'D'
    is_patient = request.user.user_type =='P'
    if request.method == 'POST':
        print(request.body)

        msg = json.loads(request.body.decode("utf-8"))
        userid = request.user.id
        _msg = Messages(receiver_id=receiver_id, sender_id=userid, message=msg.get('message'))
        _msg.save()

    messages = Messages.objects.filter(Q(sender=request.user.id, receiver=receiver_id) | Q(receiver=request.user.id, sender=receiver_id)).all()
    return render(request, "chat.html", {"messages": messages, "user_id": request.user.id, "doctor_id": receiver_id, "is_doctor": is_doctor, "is_patient": is_patient})

@login_required(login_url='/')
def get_message(request, receiver_id):
    messages = Messages.objects.filter(Q(sender=request.user.id, receiver=receiver_id) | Q(receiver=request.user.id, sender=receiver_id))
    return JsonResponse([{'message': msg.message, 'sender_id': msg.sender_id} for msg in messages], safe=False)

@login_required(login_url='/')
@user_passes_test(is_patient, login_url='/')

def inbox_page(request):

    doctors = User.objects.filter(id__in=Appointment.objects.filter(patient_id=request.user.id).values('doctor_id'))
    return render(request, "patient/inbox-page.html", {"doctors": doctors})

@login_required(login_url='/')
@user_passes_test(is_patient, login_url='/')

def listofdoctors(request, category_id):
    doctors = User.objects.filter(specialization=category_id).prefetch_related('specialization')
    return render(
        request, "patient/list-of-doctors.html", {"doctors": doctors}
    )

@login_required(login_url='/')
@user_passes_test(is_patient, login_url='/')

def categories(request):
    categories = Categories.objects.all()
    return render(
        request, "patient/categories.html", {"categories": categories}
    )

@login_required(login_url='/')
@user_passes_test(is_patient, login_url='/')

def mytreatments(request):
    return render(
        request, 'patient/mytreatments.html'
    )

@login_required(login_url='/')
@user_passes_test(is_patient, login_url='/')

def patient_prescription(request):
    presc = Prescription.objects.filter(patient_id=request.user.id)
    return render (
        request, "patient/patient-prescription.html", {'prescriptions': presc}
    )

@login_required(login_url='/')
@user_passes_test(is_patient, login_url='/')

def patient_prescription_page(request, prescription_id):
    presc = Prescription.objects.filter(id=prescription_id).first()
    return render (
        request, "patient/prescription-page.html", {'prescription' : presc}
    )

@login_required(login_url='/')
@user_passes_test(is_doctor, login_url='/')

def doctor_prescription(request):
    appoints = Appointment.objects.filter(doctor_id=request.user.id).prefetch_related('patient')
    return render (
        request, "doctor/patient-prescription.html", {'prescriptions': appoints}
    )

@login_required(login_url='/')
@user_passes_test(is_doctor, login_url='/')

def doctor_prescription_page(request, prescription_id):
    if request.method == 'POST':
        app = Appointment.objects.filter(id=prescription_id).first()
        pre = Prescription.objects.filter(id=prescription_id).first()
        presc = Prescription(
            id=prescription_id,
            patient_id=app.patient_id,
            doctor_id=request.user.id,
            details=request.POST.get('details')
        )
        if pre:
            presc.created_at = pre.created_at
        presc.save()
        return redirect('/doctor-prescription/')

    presc = Prescription.objects.filter(id=prescription_id).prefetch_related('patient').first()
    if not presc:
        presc = Appointment.objects.filter(doctor_id=request.user.id).prefetch_related('patient').first()
    return render (
        request, "doctor/prescription-page.html", {'prescription' : presc}
    )

@login_required(login_url='/')
@user_passes_test(is_admin, login_url='/')

def cashflow(request):
    if request.method == 'POST':
        input_date = request.POST.get('date')
        try:
            input_datetime = datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            input_datetime = None

        if input_datetime:
            cashflow_data = Cashflow.objects.filter(appointment_datetime__date=input_datetime.date())
        else:
            cashflow_data = None

        # Calculate total charges
        total_charges = cashflow_data.aggregate(Sum('charges'))['charges__sum'] or 0

        return render(request, 'admin/cashflow.html', {'cashflow_data': cashflow_data, 'total_charges': total_charges})

    else:
        cashflow_data = Cashflow.objects.all()

        # Calculate total charges
        total_charges = cashflow_data.aggregate(Sum('charges'))['charges__sum'] or 0

        return render(request, 'admin/cashflow.html', {'cashflow_data': cashflow_data, 'total_charges': total_charges})

