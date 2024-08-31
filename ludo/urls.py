from django.urls import path

from . import views


urlpatterns = [
    path('setamount/' , views.set_amount_view , name='setamount' ),
    path('room/' , views.RoomCode , name='room'),
    path('viewroom/' , views.ViewRoom , name='roomhtml'),
    path('viewData/<int:id>/' , views.viewData.as_view()),
    path('staff/' , views.staff_user ,name='staff'),
    path('approval-request/<int:id>/' , views.approval_request.as_view()),
    path('accept-reject/<int:id>/' , views.accept_reject_view.as_view()),
    path('win/<int:id>/' , views.result_win_view.as_view()),
    path('loss/<int:id>/' , views.result_loss_view.as_view()),
    path('cancel/<int:id>/' , views.result_cancel_view.as_view()),
    path('check-staff/', views.staffUser.as_view()),
    path('cancel-refund/<int:id>/' ,views.cancel_refund.as_view()),
    path('win-money-transfer/<int:id>/' ,views.win_money_transefer_view.as_view()),
    path('check-match/' , views.check_match)
    
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)