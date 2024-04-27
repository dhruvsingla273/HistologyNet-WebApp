import ternausnet
import ternausnet.models
import streamlit as st
import numpy as np
from PIL import Image
import io
import copy

import torch
# from torch import nn
from torchvision import transforms
from torch.optim import Adam


def load_model(path, device='cpu'): # Check for GPU or CPU
    model = ternausnet.models.UNet11() 
    # optimizer = Adam(model.parameters(), lr=0.001)
    checkpoint = torch.load(path, map_location=torch.device(device))
    model.load_state_dict(checkpoint['model_state_dict'])
    # optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    model = model.to(device)

    return model


def get_masked_image(uploaded_file, model, device='cpu'): # Check for GPU or CPU
    if st.session_state.edited == False:
        image_data = uploaded_file.read()
        input_image = Image.open(io.BytesIO(image_data))
    else:
        input_image = uploaded_file
    if input_image.mode != 'RGB':
        input_image = Image.merge("RGB", (input_image, input_image, input_image))
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()  # resizing may be needed
    ])
    input_tensor = transform(input_image).unsqueeze(0).to(device)

    model.eval()  
    with torch.no_grad():
        output_tensor = model(input_tensor)
        output_tensor = torch.sigmoid(output_tensor)
    output_numpy = output_tensor.squeeze().cpu().numpy() # Check for GPU or CPU
    output_numpy = (output_numpy > 0.5).astype(np.uint8)
    output_image = Image.fromarray(output_numpy * 255)

    return output_image


def mask_images(uploaded_files, checkpoint_path, device):
    segmented_files = []
    model = load_model(checkpoint_path, device)
    uploaded_files_copy = [copy.copy(uploaded_file) for uploaded_file in st.session_state.uploaded_files]

    for i,uploaded_file in enumerate(uploaded_files):
        segmented_file = get_masked_image(uploaded_file, model, device)
        if st.session_state.edited == True:
            shape = uploaded_files_copy[i].size
        else:
            image_data = uploaded_files_copy[i].read()
            image = Image.open(io.BytesIO(image_data))
            shape = image.size
        segmented_file = segmented_file.resize(shape)
        segmented_files.append(segmented_file)
    del uploaded_files_copy
    return segmented_files