from django.contrib import admin
from django.contrib.auth import get_user_model

from main.models import Profile, AircraftICAO, AircraftType, Agent, Penalty, SimVersion

User = get_user_model()


class ProfileAdmin(admin.TabularInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('email', 'get_full_name', 'location', 'ivao', 'vatsim')
    readonly_fields = ('password',)
    inlines = (ProfileAdmin,)
    search_fields = ('email', 'first_name', 'last_name', 'profile__ivaoid', 'profile__vatsimid')

    @admin.display
    def location(self, obj):
        return obj.profile.location

    @admin.display
    def ivao(self, obj):
        return obj.profile.ivaoid

    @admin.display
    def vatsim(self, obj):
        return obj.profile.vatsimid


admin.site.register(User, UserAdmin)


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


# class AgentAdmin(admin.ModelAdmin):
#     model = Agent
#     list_display = ('agent_version', 'agent_file')
#
#
# admin.site.register(Agent, AgentAdmin)


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
