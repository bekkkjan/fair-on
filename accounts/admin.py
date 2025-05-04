# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, EmployerProfile, CandidateProfile


class EmployerProfileInline(admin.StackedInline):
    """
    Ish beruvchi profilini foydalanuvchi sahifasida ko'rsatish
    """
    model = EmployerProfile
    can_delete = False
    verbose_name_plural = _('ish beruvchi profili')


class CandidateProfileInline(admin.StackedInline):
    """
    Nomzod profilini foydalanuvchi sahifasida ko'rsatish
    """
    model = CandidateProfile
    can_delete = False
    verbose_name_plural = _('nomzod profili')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Foydalanuvchi admin konfiguratsiyasi
    """
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_staff')
    list_filter = ('user_type', 'is_verified', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Shaxsiy ma\'lumotlar'), {'fields': ('first_name', 'last_name')}),
        (_('Ruxsatlar'), {'fields': (
        'user_type', 'is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Muhim sanalar'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'first_name', 'last_name', 'is_verified'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_inlines(self, request, obj=None):
        """
        Foydalanuvchi turiga qarab tegishli inline ko'rsatish
        """
        if obj:
            if obj.user_type == 'employer':
                return [EmployerProfileInline]
            elif obj.user_type == 'candidate':
                return [CandidateProfileInline]
        return []


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    """
    Ish beruvchi profili admin konfiguratsiyasi
    """
    list_display = ('company_name', 'get_user_full_name', 'position', 'get_is_verified')
    list_filter = ('user__is_verified',)
    search_fields = ('company_name', 'user__email', 'user__first_name', 'user__last_name')

    def get_user_full_name(self, obj):
        return obj.user.full_name

    get_user_full_name.short_description = _('F.I.O')

    def get_is_verified(self, obj):
        return obj.user.is_verified

    get_is_verified.short_description = _('Tasdiqlangan')
    get_is_verified.boolean = True


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    """
    Nomzod profili admin konfiguratsiyasi
    """
    list_display = ('get_user_full_name', 'education', 'specialization')
    list_filter = ('education',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'specialization')

    def get_user_full_name(self, obj):
        return obj.user.full_name

    get_user_full_name.short_description = _('F.I.O')