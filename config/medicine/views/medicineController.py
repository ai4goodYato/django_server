from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from ml.models.imageClassificationModel import classifyMedicineImage
from rest_framework.parsers import MultiPartParser, FormParser
import asyncio, os, requests, aiohttp

class MedicineController(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def processMedicineResponse(self, data):
        longTextDataKeyList = ["useMethodQesitm", "atpnWarnQesitm", "atpnQesitm", "intrcQesitm", "seQesitm", "depositMethodQesitm"]
        
        # 성분 추출
        itemName = data["itemName"]
        if itemName:
            ingredientAndName = list(itemName.split("("))
            if len(ingredientAndName)>1:
                ingredient = ingredientAndName[1].rstrip(")")
                data["ingredient"] = ingredient
                data["itemName"] = ingredientAndName[0]

        # 긴 텍스트 배열로 변환
        for i, text in enumerate(longTextDataKeyList):
            element = data.get(text, None)
            if element is None: continue
            elementArr = list(element.split("."))
            for i in range(len(elementArr)):
                elementStripWs = elementArr[i].strip("\n")
                elementArr[i] = elementStripWs
            data[text] = elementArr
        return data

    async def getMethodRequest(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200: # 요청 성공
                    return await response.json() # await 주의
                else: # 요청 실패
                    return None
                
    async def getMedicineApiInfo(self, name):
        urlPath = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
        accessKey=os.environ.get("MEDICINE_IDENTIFY_ACCESS_KEY")
        requestUrl=f"{urlPath}?serviceKey={accessKey}&itemName={name}&type=json"
        medicineResponse = await self.getMethodRequest(requestUrl)
        if not medicineResponse: return None
        medicineResponse = medicineResponse["body"]["items"]
        return list(map(self.processMedicineResponse, medicineResponse))
    
    def post(self, request):
        image = request.FILES.get("medicine", None)
        if image is None:
            return Response(status=400)
        
        # asyncIo로 비동기 함수 실행 + 결과 반환
        result = asyncio.run(classifyMedicineImage(image=image))
        # 이름 데이터가 없으면? : 400
        if not result['name']:
            return Response(status=400)
        # api에서 정보 받아오는게 오래걸려서 비동기처리함
        res = asyncio.run(self.getMedicineApiInfo(result["name"]))
        # 데이터 잘못받았으면? : 400
        if res is None:
            return Response(status=400)
        return Response(res)