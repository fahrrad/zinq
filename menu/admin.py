from django.contrib import admin
from menu.models import Menu, MenuItem


class MenuModelAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(MenuModelAdmin, self).queryset(request)

        return qs.filter(place__user=request.user)


class MenuItemModelAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(MenuItemModelAdmin, self).queryset(request)

        return qs.filter(menu__place__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "menu":
                kwargs["queryset"] = Menu.objects.filter(place__user=request.user)
        return super(MenuItemModelAdmin, self).formfield_for_foreignkey(db_field,
                                                                        request, **kwargs)


admin.site.register(Menu, MenuModelAdmin)
admin.site.register(MenuItem, MenuItemModelAdmin)

