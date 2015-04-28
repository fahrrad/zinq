from django.contrib import admin

from menus.models import Menu, MenuItem


class MenuModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(MenuModelAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(place__user=request.user)
        else:
            return qs



class MenuItemModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'price', 'position']
    list_filter = ('category',)
    list_editable = ('position',)

    def get_queryset(self, request):
        qs = super(MenuItemModelAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(menu__place__user=request.user)
        else:
            return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('menu')
            if db_field.name == "menus":
                kwargs["queryset"] = Menu.objects.filter(place__user=request.user)
        return super(MenuItemModelAdmin, self).formfield_for_foreignkey(db_field,
                                                                        request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.menu = Menu.objects.filter(place__user=request.user).first()

        return super(MenuItemModelAdmin, self).save_model(request, obj, form, change)

    class Media:
        js = (
            'js/admin_list_reorder.js',
        )






admin.site.register(Menu, MenuModelAdmin)
admin.site.register(MenuItem, MenuItemModelAdmin)

