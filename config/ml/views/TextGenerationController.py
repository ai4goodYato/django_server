from rest_framework.views import APIView
from rest_framework.response import Response
from ml.models.textModel import *

class TextGenerationController(APIView):
    def get(self, request):
        if not request.query_params:
            return Response(status=400)
        input_text = request.query_params.get("input_text", None)
        if input_text:
            response_text = getGeneratedText(input_text=input_text)
            return Response(response_text)
        return Response(status=400)