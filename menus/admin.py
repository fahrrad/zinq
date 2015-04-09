from adminsortable.admin import SortableAdmin
from django.contrib import admin

from menus.models import Menu, MenuItem


class MenuModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(MenuModelAdmin, self).queryset(request)
        if not request.user.is_superuser:
            return qs.filter(place__user=request.user)
        else:
            return qs


class MenuItemModelAdmin(admin.TabularInline):
    sortable_field_name = "position"

    def get_queryset(self, request):
        qs = super(MenuItemModelAdmin, self).queryset(request)
        if not request.user.is_superuser:
            return qs.filter(menu__place__user=request.user)
        else:
            return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "menus":
                kwargs["queryset"] = Menu.objects.filter(place__user=request.user)
        return super(MenuItemModelAdmin, self).formfield_for_foreignkey(db_field,
                                                                        request, **kwargs)


admin.site.register(Menu, MenuModelAdmin)
admin.site.register(MenuItem, MenuItemModelAdmin)

