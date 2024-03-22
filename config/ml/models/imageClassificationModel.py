from transformers import pipeline, ViTConfig, ViTModel, AutoImageProcessor, ViTForImageClassification, ViTFeatureExtractor
import torch
from torchvision import transforms
from transformers import AutoModelForImageClassification, AutoFeatureExtractor, AutoConfig
from PIL import Image
from io import BytesIO
import numpy as np

def classifyMedicineImage(image):
    result = None
    model_name = "pillIdentifierAI/pillIdentifier"
    imageData = Image.open(BytesIO(image.read())).convert("RGB")
    model = AutoModelForImageClassification.from_pretrained("pillIdentifierAI/pillIdentifier")
    config = AutoConfig.from_pretrained(model_name)
    class_labels = config.id2label

    # 이미지를 모델의 입력 형식으로 변환
    preprocess = transforms.Compose([
        transforms.Resize(256),  # 모델에 따라 적절한 크기로 조절
        transforms.CenterCrop(224),  # 모델에 따라 적절한 크기로 조절 (224*224만큼 가운데 잘라가는듯)
        transforms.ToTensor(),  # 이미지를 PyTorch 텐서로 변환
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # ImageNet 기준으로 정규화
    ])

    input_tensor = preprocess(imageData)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        result = model(input_batch)
    if result:
        logits_tensor = (torch.tensor(result.logits))[0] # logits라는 놈을 2차원 배열?에 담아줘서 1차원으로 갖고옴
        probabilities = torch.softmax(logits_tensor, dim=0) # softmax로 이놈을 확률로 전환
        pred_class = probabilities.argmax().item()
        # print(id2label, id2label[0])
        return {"label":class_labels[pred_class], "probability":probabilities[pred_class], "probabilities":probabilities}
    return None

def classifyImage(imageData):
    image_model_name = "google/vit-base-patch16-224"
    model_name = "pillIdentifierAI/pillIdentifier"
    # 모델 로드
    model = ViTForImageClassification.from_pretrained(model_name)
    
    # 피처 추출기 로드
    feature_extractor = ViTFeatureExtractor.from_pretrained(image_model_name)

    # 이미지 로드 및 변환
    image = Image.open(BytesIO(imageData.read())).convert("RGB")

    inputs = feature_extractor(images=image, return_tensors="pt")

    # 모델 예측
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    pred_class_idx = probabilities.argmax().item()
    
    # 클래스 라벨과 확률
    pred_label = model.config.id2label[pred_class_idx]
    pred_probability = probabilities[0, pred_class_idx].item()

    return {"label": pred_label, "probability": pred_probability, "prob":probabilities}