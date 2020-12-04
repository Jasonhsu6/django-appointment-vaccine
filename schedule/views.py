import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
# Create your views here.
from django.template.loader import render_to_string

from .forms import AppointmentForm
from .models import Appointment


def test(request):
    return render(request, "failure.html")


def index(request):
    if request.session.get("schedule_date"):
        del request.session["schedule_date"]
    if request.session.get("schedule_time"):
        del request.session["schedule_time"]
    return render(request, "index.html")


# cannot add timedelta to datetime.time
def get_time_slots():
    start = datetime.datetime(100, 1, 1, 9, 0, 0)
    slots = []
    while start.time() < datetime.time(17, 0, 0):
        slots.append(start.time().strftime("%I:%M %p"))
        start += datetime.timedelta(minutes=30)
    return slots


def check_availability(request):
    date = request.POST["schedule_date"]
    time_slots = get_time_slots()
    available = []
    for time_slot in time_slots:
        if not Appointment.objects.filter(date=date).filter(time=time_slot):
            available.append(time_slot)
    print(available)
    return available


def confirm(request):
    if request.method == "POST":
        # 'first_name', 'last_name', 'email', 'phone', 'birthday'
        info = dict()
        info["first_name"] = request.POST.get("first_name")
        info["last_name"] = request.POST.get("last_name")
        info["phone"] = request.POST.get("phone")
        info["birthday"] = request.POST.get("birthday")
        # date and time are datetime object
        info["date"] = request.session.get("schedule_date")
        info["time"] = request.session.get("schedule_time")
        info["email"] = request.POST.get("email")
        if Appointment.objects.filter(date=datetime.datetime.strptime(info["date"], "%m/%d/%Y").date().strftime("%Y-%m-%d"),
                                      time=info["time"]):
            message = "someone has already taken this appointment slot or"
            return render(request, "failure.html", context={"message": message})
        elif Appointment.objects.filter(phone=info["phone"]).count() >= 5:
            message = "you have exceeded the limit of making appointment (maximum 5 per number)"
            return render(request, "failure.html", context={"message": message})
        else:
            appointment = Appointment(
                date=datetime.datetime.strptime(info["date"], "%m/%d/%Y").date().strftime("%Y-%m-%d"),
                time=info["time"],
                first_name=info["first_name"], last_name=info["last_name"],
                email=info["email"], phone=info["phone"], birthday=info["birthday"])
            appointment.save()
            return render(request, "success.html")
            if info["email"]:
                if info["time"]:
                    send_confirmation_email(info, "appointment")
                else:
                    send_confirmation_email(info, "waitlist")
    return render(request, "confirmation.html")

# def confirm(request):
#     if request.method == "POST":
#         # 'first_name', 'last_name', 'email', 'phone', 'birthday'
#         info = dict()
#         info["first_name"] = request.POST.get("first_name")
#         info["last_name"] = request.POST.get("last_name")
#         info["email"] = request.POST.get("email")
#         info["phone"] = request.POST.get("phone")
#         info["birthday"] = request.POST.get("birthday")
#         if request.session.get("schedule_date") and request.session.get("schedule_time"):
#             # date and time are datetime object
#             info["date"] = request.session.get("schedule_date")
#             info["time"] = request.session.get("schedule_time")
#             appointment = Appointment(
#                 date=datetime.datetime.strptime(info["date"], "%m/%d/%Y").date().strftime("%Y-%m-%d"),
#                 time=info["time"],
#                 first_name=info["first_name"], last_name=info["last_name"],
#                 email=info["email"], phone=info["phone"], birthday=info["birthday"])
#             appointment.save()
#             send_confirmation_email(info, "appointment")
#
#         else:
#             if request.session.get("schedule_date"):
#                 del request.session["schedule_date"]
#             if request.session.get("schedule_time"):
#                 del request.session["schedule_time"]
#             waitlist = WaitList(first_name=info["first_name"], last_name=info["last_name"],
#                                 email=info["email"], phone=info["phone"], birthday=info["birthday"])
#             waitlist.save()
#             send_confirmation_email(info, "waitlist")
#         return render(request, "success.html")
#     return render(request, "confirmation.html")


def send_confirmation_email(info, email_type="waitlist"):
    from_email = "no_reply@alldaypharmacy"
    if email_type == "appointment":
        subject = "Confirm your appointment"
        schedule_date = datetime.datetime.strptime(info["date"], "%m/%d/%Y").date().strftime("%A, %B %d")
        schedule_time = datetime.datetime.strptime(info["time"], "%I:%M %p").time().strftime("%I:%M %p")
        html_message = render_to_string('email_appointment.html', {
            "first_name": info["first_name"],
            "last_name": info["last_name"],
            "schedule_date": schedule_date,
            "schedule_time": schedule_time
        })
        send_mail(subject, message="Confirm your appointment", from_email=from_email, recipient_list=[info["email"]],
                  html_message=html_message)
    elif email_type == "waitlist":
        subject = "Successfully joined waitlist"
        html_message = render_to_string("email_waitlist.html")
        send_mail(subject, message="You have joined waitlist", from_email=from_email, recipient_list=[info["email"]],
                  html_message=html_message)


def schedule(request):
    time_slots = get_time_slots()
    if request.method == "POST":
        if request.POST.get("schedule_date"):
            str_date = request.POST["schedule_date"]
            available = check_availability(request)
            request.session["schedule_date"] = datetime.datetime. \
                strptime(str_date, "%Y-%m-%d").date().strftime("%m/%d/%Y")
            return render(request, "schedule.html",
                          context={"time_slots": time_slots, "available": available})
        if request.POST.get("schedule_time"):
            str_time = request.POST["schedule_time"]
            request.session["schedule_time"] = str_time
            return redirect("/confirm/")
    return render(request, "schedule.html", context={"time_slots": time_slots})
