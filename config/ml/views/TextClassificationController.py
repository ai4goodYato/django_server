from rest_framework.views import APIView
from rest_framework.response import Response
from ml.models.textModel import getClassification

class TextClassificationController(APIView):
    def get(self, request):
        if not request.query_params:
            return Response(status=400)
        text = request.query_params.get('text', None)
        result = getClassification(text=text)
        return Response(result)