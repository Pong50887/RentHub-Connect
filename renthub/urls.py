from django.urls import path

from . import views

app_name = 'renthub'

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path('<str:room_type>', views.RoomTypeView.as_view(), name='room_type'),
    path('rental/', views.RoomListView.as_view(), name='rental_list'),
    path("rental/<int:room_number>/", views.RoomDetailView.as_view(), name="rental"),
    path("payment/", views.RoomPaymentListView.as_view(), name="payment_list"),
    path("payment/history", views.RoomPaymentHistoryView.as_view(), name="payment_history"),
    path("rental/<int:room_number>/payment/", views.RoomPaymentView.as_view(), name="payment"),
    path("rental/<int:room_number>/payment/submit/", views.submit_payment, name="submit"),
    path("rental/<int:room_number>/payment/cancel/", views.cancel_rental, name="cancel"),
    path('announcement/<int:pk>', views.AnnouncementView.as_view(), name="announcement"),
    path('notifications/',views.NotificationView.as_view(), name='notifications'),
    path('notifications/mark-read/', views.MarkNotificationsReadView.as_view(), name='mark_notifications_read'),

]
