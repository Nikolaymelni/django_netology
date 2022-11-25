from django.urls import path

from measurement.views import SensorView, UpdateSensorView, AddMeasurementView

urlpatterns = [
    path('sensors/', SensorView.as_view()),
    path('sensors/<pk>/', UpdateSensorView.as_view()),
    path('measurements/', AddMeasurementView.as_view())
]