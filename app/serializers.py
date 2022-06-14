from app.models import Recycler, Organization, Admin, SuspensionRequest, Alert,\
    OrganizationPerformence, PersonalDisposal, OrganizationAlerts, AlertConfirmation

from rest_framework import serializers


class RecyclerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recycler
        fields = ['username', 'email', 'password', 'phone', 'address',
                  'country', 'city', 'state']


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'org_name', 'email', 'password', 'phone', 'address',
                  'country', 'city', 'info', 'operating_locations',
                  'item_list', 'state']

class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Admin
        fields = ['email', 'user_name', 'password']

class SuspensionRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SuspensionRequest
        fields = ['email', 'request_message', 'password', 'account']


class AlertSerializer(serializers.HyperlinkedModelSerializer):
    recycler = RecyclerSerializer()
    class Meta:
        model = Alert
        fields = ['id', 'latitude', 'longitude', 'date', 'address',
                  'country', 'city', 'type', 'item_list', 'book_status',
                  'recycler']


class OrganizationPerformenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganizationPerformence
        fields = ['date', 'handled_date']

class PersonalDisposalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PersonalDisposal
        fields = ['id', 'date', 'item_list', 'type']

class OrganizationAlertsSerializer(serializers.HyperlinkedModelSerializer):
    alert = AlertSerializer()
    class Meta:
        model = OrganizationAlerts
        fields = ['id', 'date', 'alert', 'status']


class AlertConfirmationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AlertConfirmation
        fields = ['id', 'recycler_email', 'org_email', 'date', 'item_list', 'confirmation',
                  'response']