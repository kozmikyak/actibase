from django.contrib import admin

from .models import *

"""

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PlatformAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class BasePersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "job", "primary_organization")
    ordering = ("last_name", "first_name", "job" )
    list_filter = ("job",)


class RepAdmin(admin.ModelAdmin):
    list_display = ( "last_name", "first_name", "position", "get_city", "m_id",)
    ordering = ("last_name", "first_name", "position", "city_str", )
    list_filter = ("position",)


class BillAdmin(admin.ModelAdmin):
    list_display = ("number", "status",)
    ordering = ("number", )


class ActionAdmin(admin.ModelAdmin):
    list_display = ("bill_number", "date",)
    ordering = ("-date", )

    def bill_number(self, obj):
        return obj.bill.number
"""

class EventsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "calendar", "time")
    list_filter = ("calendar",)
    ordering = ("time", )

    
class OrgAdmin(admin.ModelAdmin):
    list_display = ("name", "published",)
    ordering = ("name", "published")
    list_filter = ("published", "org_type",)


#admin.site.register(Tag, TagAdmin)
#admin.site.register(Action, ActionAdmin)
#admin.site.register(PolicyRecord, BillAdmin)
#admin.site.register(BasePerson, BasePersonAdmin)
#admin.site.register(BasePerson)
#admin.site.register(PublicOfficial, RepAdmin)
#admin.site.register(Org, OrgAdmin)
#admin.site.register(SocialOutput)
#admin.site.register(dx_City)
#admin.site.register(dx_County)
#admin.site.register(dx_State)
#admin.site.register(dx_PostalCode)
#admin.site.register(Platform, PlatformAdmin)
#admin.site.register(dx_District)
#admin.site.register(Events, EventsAdmin)
