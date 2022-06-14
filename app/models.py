from django.db import models
import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField

class Recycler(models.Model):
    username = models.TextField(unique=True)
    email = models.TextField(unique=True)
    password = models.TextField()
    phone = models.TextField(unique=True)
    address = models.TextField()
    country = models.TextField()
    city = models.TextField()
    SUSPENDED = 'S'
    ACTIVATED = 'A'
    STATE_CHOICES = [
        (SUSPENDED, 'Suspended'),
        (ACTIVATED, 'Activated')
    ]
    state = models.CharField(
        max_length=1,
        choices=STATE_CHOICES,
        default=ACTIVATED
    )

    def __str__(self):
        return self.username


class PersonalDisposal(models.Model):
    recycler = models.ForeignKey(Recycler, on_delete=models.CASCADE)
    item_list = models.TextField()
    date = models.DateField(default=datetime.date.today)
    PUBLIC = 'PUB'
    PERSONAL = 'PER'
    UNREPORTED = 'SAV'
    TYPE_CHOICES = [
        (PUBLIC, 'Public'),
        (PERSONAL, 'Personal'),
        (UNREPORTED, 'Unreported')
    ]

    type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default=PERSONAL
    )
    def __str__(self):
        return self.item_list


class Alert(models.Model):
    recycler = models.ForeignKey(Recycler, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    item_list = models.TextField()
    date = models.DateField(default=datetime.date.today)
    address = models.TextField()
    country = models.TextField()
    city = models.TextField()
    PUBLIC = 'PUB'
    PERSONAL = 'PER'
    TYPE_CHOICES = [
        (PUBLIC, 'Public'),
        (PERSONAL, 'Personal')
    ]
    type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default=PERSONAL
    )
    BOOKED = 'B'
    UNBOOKED = 'UB'
    BOOK_CHOICES = [
        (BOOKED, 'Booked'),
        (UNBOOKED, 'Unbooked')
    ]
    book_status = models.CharField(
        max_length=2,
        choices=BOOK_CHOICES,
        default=UNBOOKED
    )

    def __str__(self):
        return self.item_list

class Organization(models.Model):
    org_name = models.TextField(unique=True)
    password = models.TextField()
    phone = models.TextField(unique=True)
    email = models.TextField(unique=True)
    address = models.TextField()
    country = models.TextField()
    city = models.TextField()
    info = models.TextField()
    operating_locations = models.TextField()
    item_list = models.TextField()
    SUSPENDED = 'S'
    ACTIVATED = 'A'
    STATE_CHOICES = [
        (SUSPENDED, 'Suspended'),
        (ACTIVATED, 'Activated')
    ]
    state = models.CharField(
        max_length=1,
        choices=STATE_CHOICES,
        default=ACTIVATED
    )

    def __str__(self):
        return self.org_name


class OrganizationAlerts(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    HANDLED = 'H'
    UNHANDLED = 'U'
    STATUS_CHOICES = [
        (HANDLED, 'Handled'),
        (UNHANDLED, 'Unhandled')
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=UNHANDLED
    )

    def __str__(self):
        return self.item_list + self.status

class OrganizationPerformence(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField()
    handled_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.organization

class Admin(models.Model):
    email = models.TextField()
    user_name = models.TextField()
    password = models.TextField()

    def __str__(self):
        return self.user_name + ":admin"


class SuspensionRequest(models.Model):
    email = models.TextField()
    request_message = models.TextField()
    password = models.TextField()
    ORGANIZATION = 'O'
    STANDARD = 'S'
    ACCOUNT_CHOICES = [
        (ORGANIZATION, 'Organization'),
        (STANDARD, 'Standard')
    ]
    account = models.CharField(
        max_length=1,
        choices=ACCOUNT_CHOICES,
        default=ORGANIZATION
    )

    def __str__(self):
        return self.request_message


class AlertConfirmation(models.Model):
    recycler_email = models.TextField()
    org_email = models.TextField()
    date = models.DateField(default=datetime.date.today)
    item_list = models.TextField(default=None)
    CHECKED = 'C'
    UNCHECKED = 'U'
    CONFIRMATION_CHOICES = [
        (CHECKED, 'Checked'),
        (UNCHECKED, 'Unchecked')
    ]
    confirmation = models.CharField(
        max_length=2,
        choices=CONFIRMATION_CHOICES,
        default=UNCHECKED
    )

    HANDLED = 'H'
    UNHANDLED = 'UH'
    INCONCLUSIVE = 'IN'
    RESPONSE_CHOICES = [
        (HANDLED, 'Handled'),
        (UNHANDLED, 'Unhandled'),
        (INCONCLUSIVE, 'Inconclusive')
    ]
    response = models.CharField(
        max_length=2,
        choices=RESPONSE_CHOICES,
        default=INCONCLUSIVE
    )

class OrgPhoto(models.Model):
    image = CloudinaryField('image')
    caption = models.CharField(max_length=100, blank=True)

class AlertPhoto(models.Model):
    image = CloudinaryField('image')
    caption = models.CharField(max_length=100, blank=True)
