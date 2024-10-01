from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, PhishingLink, PhishingData

admin.site.register(User)
admin.site.register(PhishingLink)
admin.site.register(PhishingData)
