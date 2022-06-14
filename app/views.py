from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from app.models import Recycler, Organization, Admin, SuspensionRequest, Alert,\
    OrganizationPerformence, OrganizationAlerts, PersonalDisposal, AlertConfirmation, OrgPhoto, AlertPhoto
from app.serializers import RecyclerSerializer, OrganizationSerializer, \
    AdminSerializer, SuspensionRequestSerializer, AlertSerializer,\
    OrganizationPerformenceSerializer, PersonalDisposalSerializer,\
    OrganizationAlertsSerializer, AlertConfirmationSerializer
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import OrgPhotoForm, AlertPhotoForm

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("Hello, world. You're at the recycleit app.")


@csrf_exempt
def add_recycler(request):
    recycler = Recycler(username=request.GET.get('username'),
                        email=request.GET.get('email'),
                        password=request.GET.get('password'),
                        phone=request.GET.get('phone'),
                        address=request.GET.get('address'),
                        country=request.GET.get('country'),
                        city=request.GET.get('city'))
    recycler.save()
    data = {'result': 'ok', }
    return JsonResponse(data, safe=False)

def get_recycler(request):
    if request.method == 'GET':
        emal = request.GET.get("email")
        recycler = Recycler.objects.filter(email=emal)
        serializer = RecyclerSerializer(recycler, many=True)
        return JsonResponse(serializer.data, safe=False)

def verify_r_email(request):
    if request.method == 'GET':
        emal = request.GET.get("email")
        recycler = Recycler.objects.filter(email=emal)
        if recycler.exists():
            return JsonResponse("{'result': 'ok'}", safe=False)

        return JsonResponse("{'result': 'no'}", safe=False)

def verify_r_username(request):
    if request.method == 'GET':
        username = request.GET.get("username")
        recycler = Recycler.objects.filter(username=username)
        if recycler.exists():
            return JsonResponse("{'result': 'ok'}", safe=False)

        return JsonResponse("{'result': 'no'}", safe=False)

def verify_r_phone(request):
    if request.method == 'GET':
        phone = request.GET.get("phone")
        recycler = Recycler.objects.filter(phone=phone)
        if recycler.exists():
            return JsonResponse("{'result': 'ok'}", safe=False)

        return JsonResponse("{'result': 'no'}", safe=False)

def verify_org_email(request):
    if request.method == 'GET':
        emal = request.GET.get("email")
        org = Organization.objects.filter(email=emal)
        if org.exists():
            return JsonResponse("{'result': 'ok'}", safe=False)

        return JsonResponse("{'result': 'no'}", safe=False)

def verify_org_username(request):
    if request.method == 'GET':
        username = request.GET.get("org_name")
        org = Organization.objects.filter(org_name=username)
        if org.exists():
            return JsonResponse("{'result': 'ok'}", safe=False)

        return JsonResponse("{'result': 'no'}", safe=False)

def verify_org_phone(request):
    if request.method == 'GET':
        phone = request.GET.get("phone")
        org = Organization.objects.filter(phone=phone)
        if org.exists():
            return JsonResponse("{'result': 'ok'}", safe=False)

        return JsonResponse("{'result': 'no'}", safe=False)


def add_org(request):
    organization = Organization(org_name=request.GET.get('orgname'),
                        email=request.GET.get('email'),
                        password=request.GET.get('password'),
                        phone=request.GET.get('phone'),
                        address=request.GET.get('address'),
                        country=request.GET.get('country'),
                        city=request.GET.get('city'),
                        info=request.GET.get('info'),
                        operating_locations=request.GET.get('oploc'),
                        item_list=request.GET.get('item_list')
                                )
    organization.save()
    data = {'result': 'ok', }
    return JsonResponse(data, safe=False)

def get_org(request):
    if request.method == 'GET':
        emal = request.GET.get("email")
        organization = Organization.objects.filter(email=emal)
        serializer = OrganizationSerializer(organization, many=True)
        return JsonResponse(serializer.data, safe=False)

def login_recycler(request):
    emal = request.GET.get("email")
    passw = request.GET.get("password")

    user = Recycler.objects.filter(email=emal, password=passw).values()
    data=""
    if user.exists():
        data = list(user)
    else:
        data = "{'result': 'no'}"

    return JsonResponse(data, safe=False)

def login_org(request):
    emal = request.GET.get("email")
    passw = request.GET.get("password")

    user = Organization.objects.filter(email=emal, password=passw).values()
    data=""
    if user.exists():
        data = list(user)
    else:
        data = "{'result': 'no'}"

    return JsonResponse(data, safe=False)

def login_admin(request):
    emal = request.GET.get("email")
    passw = request.GET.get("password")

    user = Admin.objects.filter(email=emal, password=passw).values()
    data=""
    if user.exists():
        data = list(user)
    else:
        data = "{'result': 'no'}"

    return JsonResponse(data, safe=False)


def suspend_recycler(request):
    emal = request.GET.get("email")
    state = request.GET.get("state")

    recycler = Recycler.objects.get(email=emal)

    recycler.state = state
    recycler.save()
    data = {'result': 'ok'}

    return JsonResponse(data, safe=False)

def suspend_org(request):
    emal = request.GET.get("email")
    state = request.GET.get("state")
    account = request.GET.get("account")

    if account == 'O':
        org = Organization.objects.get(email=emal)
        org.state = state
        org.save()
    else:
        recycler = Recycler.objects.get(email=emal)
        recycler.state = state
        recycler.save()

    if SuspensionRequest.objects.filter(email=emal).exists():
        SuspensionRequest.objects.filter(email=emal).delete()
    message = Mail(
        from_email='abdullahjaffer96@gmail.com',
        to_emails=emal,
        subject='Account Status',
        html_content='<strong>Dear User, '
                     'we wanted to notify you that your request to '
                     'deactivate your account has been approved, contact '
                     'our site manager at abdullahjaffer96@gmail.com'
                     ' for further information</strong>')
    try:
        sg = SendGridAPIClient('apikey')
        response = sg.send(message)
    except Exception as e:
        print(e.message)

    data = {'result': 'ok'}

    return JsonResponse(data, safe=False)


def cancel_suspend(request):
    emal = request.GET.get("email")

    message = Mail(
        from_email='abdullahjaffer96@gmail.com',
        to_emails=emal,
        subject='Account Status',
        html_content='<strong>Dear User, '
                     'we wanted to notify you that your request to '
                     'deactivate your account has unfortunately '
                     'been rejected, contact '
                     'our site manager at abdullahjaffer96@gmail.com'
                     ' for further information</strong>')
    try:
        sg = SendGridAPIClient('apikey')
        response = sg.send(message)
    except Exception as e:
        print(e.message)

    data = {'result': 'ok'}

    return JsonResponse(data, safe=False)

def send_code(request):
    emal = request.GET.get("email")
    code = request.GET.get("code")
    message = Mail(
        from_email='abdullahjaffer96@gmail.com',
        to_emails=emal,
        subject='Your Code',
        html_content='<strong>Dear User, '
                     'your code is ' + str(code) +
                     ' for further information contact abdullahjaffer96@gmail.com</strong>')
    try:
        sg = SendGridAPIClient('apikey')
        response = sg.send(message)
    except Exception as e:
        print(e.message)

    data = {'result': 'ok'}

    return JsonResponse(data, safe=False)


def suspend_reqs(request):
    if request.method == 'GET':
        sr = SuspensionRequest.objects.all()
        serializer = SuspensionRequestSerializer(sr, many=True)
        return JsonResponse(serializer.data, safe=False)

def add_sus_rep(request):
    sr = SuspensionRequest(
                        email=request.GET.get('email'),
                        request_message=request.GET.get('reqmsg'),
                        password=request.GET.get('password'),
                        account=request.GET.get('account')
                                )
    sr.save()
    data = {'result': 'ok', }
    return JsonResponse(data, safe=False)


def update_org(request):
    emal1 = request.GET.get("email1")
    org = Organization.objects.get(email=emal1)
    org.org_name = request.GET.get('orgname')
    org.email = request.GET.get('email2')
    org.password = request.GET.get('password')
    org.phone = request.GET.get('phone')
    org.address = request.GET.get('address')
    org.country = request.GET.get('country')
    org.city = request.GET.get('city')
    org.info = request.GET.get('info')
    org.operating_locations = request.GET.get('oploc')
    org.item_list = request.GET.get('item_list')
    org.save()
    data = {'result': 'ok'}

    return JsonResponse(data, safe=False)

def update_rec(request):
    emal1 = request.GET.get("email1")
    recycler = Recycler.objects.get(email=emal1)
    recycler.username = request.GET.get('username')
    recycler.email = request.GET.get('email2')
    recycler.password = request.GET.get('password')
    recycler.phone = request.GET.get('phone')
    recycler.address = request.GET.get('address')
    recycler.country = request.GET.get('country')
    recycler.city = request.GET.get('city')
    recycler.save()
    data = {'result': 'ok'}

    return JsonResponse(data, safe=False)


def add_alert(request):
    email = request.GET.get('recemail')
    recycler = Recycler.objects.get(email=email)

    if 'book' in request.GET:
        alert = Alert(recycler=recycler,
                      latitude=request.GET.get('latitude'),
                      longitude=request.GET.get('longitude'),
                      address=request.GET.get('address'),
                      country=request.GET.get('country'),
                      city=request.GET.get('city'),
                      type=request.GET.get('type'),
                      item_list=request.GET.get('item_list'),
                      book_status=request.GET.get('book')
                      )
        alert.save()
    else:
        alert = Alert(recycler=recycler,
                            latitude=request.GET.get('latitude'),
                            longitude=request.GET.get('longitude'),
                            address=request.GET.get('address'),
                            country=request.GET.get('country'),
                            city=request.GET.get('city'),
                            type=request.GET.get('type'),
                            item_list=request.GET.get('item_list')
                                    )
        alert.save()

    data = {'result': 'ok', }
    return JsonResponse(data, safe=False)


def get_all_alerts(request):
    if request.method == 'GET':
        alert = Alert.objects.all()
        serializer = AlertSerializer(alert, many=True)
        return JsonResponse(serializer.data, safe=False)

def get_alert(request):
    id = request.GET.get("id")

    alert = Alert.objects.filter(id=id).values()
    data = ""
    if alert.exists():
        data = list(alert)
    else:
        data = "{'result': 'no'}"

    return JsonResponse(data, safe=False)

def get_org_performence(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        org = Organization.objects.get(email=email)
        performence = OrganizationPerformence.objects.filter(organization=org)
        serializer = OrganizationPerformenceSerializer(performence, many=True)
        return JsonResponse(serializer.data, safe=False)

def add_org_performence(request):
    email = request.GET.get('orgmail')
    organization = Organization.objects.get(email=email)
    alert = OrganizationPerformence(organization=organization, date=request.GET.get('date'))
    alert.save()
    data = {'result': 'ok', }
    return JsonResponse(data, safe=False)

def add_disposal_info(request):
    email = request.GET.get('email')
    recycler = Recycler.objects.get(email=email)
    per = PersonalDisposal(
        recycler=recycler, item_list=request.GET.get('item_list'),
        type=request.GET.get('type'))
    per.save()
    data = {'result': 'ok', }
    return JsonResponse(data, safe=False)

def get_disposal_info(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        r = Recycler.objects.get(email=email)
        info = PersonalDisposal.objects.filter(recycler=r)
        serializer = PersonalDisposalSerializer(info, many=True)
        return JsonResponse(serializer.data, safe=False)

def add_org_alert(request):
    email = request.GET.get('email')
    alertid = request.GET.get('alertid')
    org = Organization.objects.get(email=email)
    alert = Alert.objects.get(id=alertid)
    alert.book_status = 'B'
    alert.save()
    oa = OrganizationAlerts(organization=org,
                             alert=alert)
    oa.save()
    data = {'result': 'ok', }
    return JsonResponse(data, safe=False)

def unbook_alert(request):
    id = request.GET.get("id")
    o_alert = OrganizationAlerts.objects.get(id=id)
    o_alert.alert.book_status = 'UB'
    o_alert.alert.save()
    o_alert.save()
    data = {'result': 'ok'}

    return JsonResponse(data, safe=False)


def change_org_alert_status(request):
    id = request.GET.get("id")
    status = request.GET.get("status")
    alert = OrganizationAlerts.objects.get(id=id)
    alert.status = status
    alert.save()
    data = {'result': 'ok'}

    return JsonResponse(data, safe=False)

def get_org_alerts(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        org = Organization.objects.get(email=email)
        alerts = OrganizationAlerts.objects.filter(organization=org)
        serializer = OrganizationAlertsSerializer(alerts, many=True)
        return JsonResponse(serializer.data, safe=False)


def get_rec_alerts(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        recycler = Recycler.objects.get(email=email)
        alerts = Alert.objects.filter(recycler=recycler)
        serializer = AlertSerializer(alerts, many=True)
        return JsonResponse(serializer.data, safe=False)


def get_rec_alert_conf(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        alerts = AlertConfirmation.objects.filter(recycler_email=email, confirmation='U')
        serializer = AlertConfirmationSerializer(alerts, many=True)
        return JsonResponse(serializer.data, safe=False)

def get_org_alert_conf(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        alerts = AlertConfirmation.objects.filter(org_email=email)
        serializer = AlertConfirmationSerializer(alerts, many=True)
        return JsonResponse(serializer.data, safe=False)


def update_alert_conf(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        response = request.GET.get('response')
        alert = AlertConfirmation.objects.get(id=id)
        alert.confirmation = 'C'
        alert.response = response
        alert.save()
        data = {'result': 'ok'}
        return JsonResponse(data, safe=False)

def add_alert_conf(request):
    if request.method == 'GET':
        alert_confirmation = AlertConfirmation(
            recycler_email=request.GET.get('rec_email'),
            org_email=request.GET.get('org_email'),
            date=request.GET.get('date'),
            item_list=request.GET.get('item_list'),
            confirmation=request.GET.get('confirmation'),
            response=request.GET.get('response'))
        alert_confirmation.save()
        data = {'result': 'ok'}
        return JsonResponse(data, safe=False)

def add_org_photo(request):
    # cloudinary.config(
    #    cloud_name = 'abdullahajaffer96',
    #    api_key = '635123897871638',
    #    api_secret = 'qvzbFzB728rsixBcuvfL02rmcT4'
    # )
    if request.method == "POST":
        form = OrgPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = OrgPhoto()
            photo.caption = request.POST.get('caption')
            photo.save()
            email = request.POST.get('email')
            id = Organization.objects.get(email=email).id
            result = cloudinary.uploader.upload(request.FILES['image'],
                                                public_id ='org'+str(id),
                                                invalidate=True)
            data = {'result': 'ok'}
            return JsonResponse(data, safe=False)
    else:
        form = OrgPhotoForm()

    return render(request, 'add-photo.html', {'form': form})

def add_alert_photo(request):
    # cloudinary.config(
    #    cloud_name = 'abdullahajaffer96',
    #    api_key = '635123897871638',
    #    api_secret = 'qvzbFzB728rsixBcuvfL02rmcT4'
    # )
    if request.method == "POST":
        form = AlertPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = AlertPhoto()
            photo.caption = request.POST.get('caption')
            photo.save()
            id = Alert.objects.latest('id').id
            result = cloudinary.uploader.upload(request.FILES['image'],
                                                public_id='alert' + str(id),
                                                invalidate=True)
            data = {'result': 'ok'}
            return JsonResponse(data, safe=False)
    else:
        form = AlertPhotoForm()

    return render(request, 'add-photo.html', {'form': form})