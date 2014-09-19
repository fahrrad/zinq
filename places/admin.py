from menus.models import Menu

__author__ = 'ward'

from django.contrib import admin
from places.models import Table, Place


# only show the tables from places linked to the current user
class PlaceModelAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url='', extra_context=None):

        if not request.user.is_superuser:
            self.exclude = ('user',)
        return super(PlaceModelAdmin, self).add_view(request, form_url, extra_context)

    def queryset(self, request):
        qs = super(PlaceModelAdmin, self).queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        else:
            return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "menus":
                kwargs["queryset"] = Menu.objects.filter(place__user=request.user)
        return super(PlaceModelAdmin, self).formfield_for_foreignkey(db_field,
                                                                     request, **kwargs)


# only show the tables from places linked to the current user
class TableModelAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(TableModelAdmin, self).queryset(request)
        if not request.user.is_superuser:
            return qs.filter(place__user=request.user)
        else:
            return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "places":
            kwargs["queryset"] = Place.objects.filter(user=request.user)
        return super(TableModelAdmin, self).formfield_for_foreignkey(db_field,
                                                                     request, **kwargs)

        # needed for easy test
        # exclude = ("uuid",)


admin.site.register(Place, PlaceModelAdmin)
admin.site.register(Table, TableModelAdmin)

