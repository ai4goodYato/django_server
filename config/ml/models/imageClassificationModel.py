from transformers import pipeline, ViTConfig, ViTModel, AutoImageProcessor, ViTForImageClassification, ViTFeatureExtractor
import torch
from torchvision import transforms
from transformers import AutoModelForImageClassification, AutoFeatureExtractor, AutoConfig
from PIL import Image
from io import BytesIO
import numpy as np

async def classifyMedicineImage(image):
    return {"name":"타이레놀"}
