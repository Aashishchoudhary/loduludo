from django.contrib import admin

from .models import Payment_deposit ,Payment_withdrwable

@admin.register(Payment_deposit , Payment_withdrwable )
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]