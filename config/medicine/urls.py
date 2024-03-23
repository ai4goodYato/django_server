from django.urls import path
from medicine.views.medicineController import MedicineController

urlpatterns = [
    path("", MedicineController.as_view())
]