from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import TokenProxy
from main.models import Profile, AircraftICAO, AircraftType, Agent, Penalty, SimVersion


# Register your models here.

# admin.site.unregister(User)
# admin.site.unregister(Group)

# class CustomUserAdmin(admin.ModelAdmin):
#     model = User
#     list_display = ('email','first_name','last_name')
#     def has_add_permission(self, request):
#         return False
#     def has_change_permission(self, request, obj=None):
#         return True
#     def has_delete_permission(self, request, obj=None):
#         return False

# admin.site.register(User,CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'location', 'flights', 'hours', 'ivaoid', 'vatsimid', 'telegram_chat_id')


admin.site.register(Profile, ProfileAdmin)


class AircraftTypeAdmin(admin.ModelAdmin):
    model = AircraftType
    list_display = ('aircraft_icao', 'aircraft_name', 'engine_type')


# admin.site.register(AircraftType, AircraftTypeAdmin)


class AircraftTypeInlineAdmin(admin.TabularInline):
    model = AircraftType


class AircraftICAOAdmin(admin.ModelAdmin):
    model = AircraftICAO
    list_display = ('aircraft_icao', 'flaps10', 'flaps15', 'flaps35', 'max_pitch')
    inlines = [AircraftTypeInlineAdmin]

    class Meta:
        verbose_name = 'Aircraft Type'
        verbose_name_plural = 'Aircraft Types'


admin.site.register(AircraftICAO, AircraftICAOAdmin)


class AgentAdmin(admin.ModelAdmin):
    model = Agent
    list_display = ('agent_version', 'agent_file')


admin.site.register(Agent, AgentAdmin)


class PenaltyAdmin(admin.ModelAdmin):
    model = Penalty
    list_display = ('id', 'name', 'rate')

    # def has_change_permission(self, request, obj=None):
    #     return False
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Penalty, PenaltyAdmin)


class SimVersionAdmin(admin.ModelAdmin):
    model = SimVersion


admin.site.register(SimVersion, SimVersionAdmin)
