from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from ml.models.imageClassificationModel import classifyMedicineImage
from ml.models.classifyPillImage import classifyPillImage
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from io import BytesIO
import asyncio, os, aiohttp

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

        if data["itemName"] == "리치칼슘연질캡슐":
            data["intrcQesitm"]="이 약을 먹을 때는 칼슘, 비타민 D, 마그네슘 같은 보충제나 물을 많이 빼는 약(이뇨제)와 함께 먹지 마세요. 또 심장약, 콜레스테롤 낮추는 약, 변비약, 위산 줄이는 약, 발작이나 염증을 다스리는 약, 피임약 같은 다른 약을 먹고 있다면, 의사나 약사와 한번 상의해 보세요."
            data["atpnQesitm"]="이 약은 몸에 특정한 건강 상태가 있는 분들은 드시면 안 됩니다. 예를 들어, 몸 속에 칼슘, 인산염, 마그네슘 수치가 너무 높은 분, 혈액이 너무 알칼리성인 분(우유를 너무 많이 마셔서 생기는 증상이나 Burnett 증후군이 있는 분), 비타민 D를 너무 많이 섭취해서 문제가 생긴 분은 이 약을 피해야 합니다. 또한, 임신 중이거나 임신할 가능성이 있는 여성, 수유 중인 여성, 어린이, 나이가 많으신 분, 신장결석을 겪어본 분, 유육종증이 있는 분, 황색5호에 알레르기가 있는 분도 의사나 약사와 상의하셔야 합니다. 약을 드실 때는 정해진 방법과 양을 잘 지키고, 의사가 칼슘 섭취에 대해 주신 지시를 잘 따라주십시오."
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
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200: # 요청 성공
                        return await response.json() # await 주의
                    else: # 요청 실패
                        return None
        except:
            return None
                
    async def getMedicineApiInfo(self, name):
        try:
            urlPath = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
            accessKey=os.environ.get("MEDICINE_IDENTIFY_ACCESS_KEY")
            requestUrl=f"{urlPath}?serviceKey={accessKey}&itemName={name}&type=json"
            medicineResponse = await self.getMethodRequest(requestUrl)
            if not medicineResponse: return None
            medicineResponse = medicineResponse["body"]["items"]
            return list(map(self.processMedicineResponse, medicineResponse))
        except:
            return None
    
    def post(self, request):
        image = request.FILES.get("medicine", None)
        if image is None:
            return Response({
                "status":400,
                "message":"image not exist"
            })
        image = Image.open(BytesIO(image.read()))
        if image.mode == "RGBA":
            image = image.convert("RGB")
        
        # asyncIo로 비동기 함수 실행 + 결과 반환
        # result = asyncio.run(classifyMedicineImage(image=image))
        result = classifyPillImage(image)
        # 이름 데이터가 없으면? : 400
        if not result['name']:
            return Response({"status":400, "message":"pill name not exist"})
        # api에서 정보 받아오는게 오래걸려서 비동기처리함
        res = asyncio.run(self.getMedicineApiInfo(result["name"]))
        # 데이터 잘못받았으면? : 400
        if res is None:
            return Response({"status":400, "message":"api data get failed"})
        return Response(res)