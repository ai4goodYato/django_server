from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from ml.models.imageClassificationModel import classifyMedicineImage, classifyImage
from PIL import Image

class ImageClassificationController(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if not "image" in request.FILES:
            print("image not exist")
            return Response(status=400)
        image = request.FILES.get("image", None)
        print(image, type(image)    )
        # result = classifyMedicineImage(image=image)
        result = classifyImage(imageData=image)
        if result is None: 
            return Response(status=400)
        return Response(result)