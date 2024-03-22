from django.urls import path
from ml.views.TextGenerationController import TextGenerationController
from ml.views.TextClassificationController import TextClassificationController
from ml.views.ImageClassificationController import ImageClassificationController

urlpatterns = [
    path('classification/', TextClassificationController.as_view()),
    path('textGeneration/', TextGenerationController.as_view()),
    path('imageClassification/', ImageClassificationController.as_view()),
]