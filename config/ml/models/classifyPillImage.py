import torch
import numpy as np
import matplotlib.pyplot as plt
import torch
from torchvision import transforms
from PIL import Image
import timm  # 예를 들어, timm 라이브러리를 사용해 모델을 로드할 경우
from os import path
import cv2
import pytesseract
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from config.settings import BASE_DIR


def classifyPillImage(imageInput):
    model = timm.create_model('resnet18', pretrained=False, num_classes=11)
    checkpoint_path = str(BASE_DIR) + "/ml/models/shape.ckpt"
    model.load_state_dict(torch.load(checkpoint_path, map_location='cpu'))
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    # image_path = "C:/Users/kym8821/Desktop/코딩용/django/django_server/config/ml/models/pill.jpg"
    # image = Image.open(image_path)
    image = transform(imageInput).unsqueeze(0)
    model.eval()
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
    pill_types = [
        "알약_원형",
        "알약_장방형or타원형",
        "알약_기타",
        "알약_팔각형",
        "알약_삼각형",
        "알약_사각형",
        "알약_오각형",
        "알약_육각형",
        "알약_마름모형",
        "캡슐_장방형or타원형",
        "캡슐_기타",
    ]
    pills_prediction = predicted.item()
    # pill_type = pill_types.index(pills_prediction)
    comparison_list = [100, 18, 12]
    # # 이미지를 그레이스케일로 변환합니
    # image2 = cv2.imread(image_path)
    # gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    # # Canny 엣지 검출기를 사용해 엣지를 검출합니다
    # edges = cv2.Canny(gray, threshold1=30, threshold2=100)
    # # 검출된 엣지를 기반으로 이진화 이미지를 생성합니다
    # # 엣지가 있는 부분은 흰색(255), 그렇지 않은 부분은 검은색(0)으로 설정합니다
    # binary_image = np.zeros_like(edges)
    # binary_image[edges > 0] = 255
    # binary_image = cv2.cvtColor(binary_image, cv2.COLOR_BGR2RGB)
    # im_pil = Image.fromarray(binary_image)
    # extractedInformation = pytesseract.image_to_string(im_pil)
    df = pd.read_excel(str(BASE_DIR) + "/ml/models/openData.xls")
    df_new = df[['의약품제형', '품목명', '색상앞', '표시앞']]
    for index, row in df_new.iterrows():
        color = df_new.at[index, '색상앞']
        if color == "갈색" or color == "빨강" or color == "자주" or color == "검정":
            df_new.at[index, '색상앞'] = 0
        elif color == "갈색, 투명":
            df_new.at[index, '색상앞'] = 1
        elif color == "남색" or color == "보라":
            df_new.at[index, '색상앞'] = 2
        elif color == "노랑" or color == "주황":
            df_new.at[index, '색상앞'] = 3
        elif color == "노랑, 투명":
            df_new.at[index, '색상앞'] = 4
        elif color == "보라, 투명":
            df_new.at[index, '색상앞'] = 5
        elif color == "분홍":
            df_new.at[index, '색상앞'] = 6
        elif color == "분홍, 투명":
            df_new.at[index, '색상앞'] = 7
        elif color == "빨강, 투명":
            df_new.at[index, '색상앞'] = 8
        elif color == "연두" or color == "초록" or color == "청록":
            df_new.at[index, '색상앞'] = 9
        elif color == "연두, 투명":
            df_new.at[index, '색상앞'] = 10
        elif color == "주황, 투명":
            df_new.at[index, '색상앞'] = 11
        elif color == "청록, 투명":
            df_new.at[index, '색상앞'] = 12
        elif color == "초록, 투명":
            df_new.at[index, '색상앞'] = 13
        elif color == "투명":
            df_new.at[index, '색상앞'] = 14
        elif color == "파랑":
            df_new.at[index, '색상앞'] = 15
        elif color == "파랑, 투명":
            df_new.at[index, '색상앞'] = 16
        elif color == "하양" or color == "하양, 갈색":
            df_new.at[index, '색상앞'] = 17
        elif color == "하양, 노랑":
            df_new.at[index, '색상앞'] = 18
        elif color == "하양, 파랑":
            df_new.at[index, '색상앞'] = 19
        elif color == "회색" or color == "하양, 투명":
            df_new.at[index, '색상앞'] = 20
        else:
            df_new.at[index, '색상앞'] = 20
        shape = df_new.at[index, '의약품제형']
        if '캡슐' or '캅셀' in df_new.at[index, '품목명']:
            if shape == "원형":
                df_new.at[index, '의약품제형'] = 0
            elif shape == "장방형" or shape == "타원형":
                df_new.at[index, '의약품제형'] = 1
            elif shape == "기타":
                df_new.at[index, '의약품제형'] = 2
            elif shape == "팔각형":
                df_new.at[index, '의약품제형'] = 3
            elif shape == "삼각형":
                df_new.at[index, '의약품제형'] = 4
            elif shape == "사각형":
                df_new.at[index, '의약품제형'] = 5
            elif shape == "오각형":
                df_new.at[index, '의약품제형'] = 6
            elif shape == "육각형":
                df_new.at[index, '의약품제형'] = 7
            elif shape == "마름모형":
                df_new.at[index, '의약품제형'] = 8
            else:
                df_new.at[index, '의약품제형'] = 10
        else:
            if shape == "장방형" or shape == "타원형":
                df_new.at[index, '의약품제형'] = 9
            else:
                df_new.at[index, '의약품제형'] = 10
        df_new.at[index, '표시앞'] = 0
    del df_new['품목명']

    # comparison_list = [3, 18, 0]

    cosine_similarities = cosine_similarity(df_new.values, [comparison_list])
    df_new['cosine_similarity'] = cosine_similarities
    most_similar_row = df.loc[df_new['cosine_similarity'].idxmax()]
    similarity = df_new.loc[df_new['cosine_similarity'].idxmax()]
    print(most_similar_row)
    return {"name":most_similar_row["품목명"], "similarity":similarity}