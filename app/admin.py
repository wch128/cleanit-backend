from django.contrib import admin
from app.models import Recycler, Organization, Admin, SuspensionRequest, Alert,\
    OrganizationPerformence, OrganizationAlerts, PersonalDisposal, AlertConfirmation,\
    OrgPhoto, AlertPhoto

@admin.register(Recycler)
class RecyclerAdmin(admin.ModelAdmin):
    pass

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    pass


@admin.register(SuspensionRequest)
class SuspensionRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(OrganizationPerformence)
class OrganizationPerformenceAdmin(admin.ModelAdmin):
    pass

@admin.register(OrganizationAlerts)
class OrganizationAlertsAdmin(admin.ModelAdmin):
    pass

@admin.register(PersonalDisposal)
class PersonalDisposalAdmin(admin.ModelAdmin):
    pass

@admin.register(AlertConfirmation)
class AlertConfirmationAdmin(admin.ModelAdmin):
    pass

@admin.register(OrgPhoto)
class OrgPhotoAdmin(admin.ModelAdmin):
    pass

@admin.register(AlertPhoto)
class AlertPhotoAdmin(admin.ModelAdmin):
    pass