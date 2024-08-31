from django.contrib import admin

from .models import Price , Price_cut , Room , result_win , result_cancel , result_loss ,match_deposit_payment , match_withdrawl_payment
# Register your models here.
@admin.register(Price , Price_cut , Room , result_win , result_cancel , result_loss ,match_withdrawl_payment ,match_deposit_payment)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]