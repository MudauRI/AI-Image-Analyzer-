import gradio as gr
from PIL import Image, ImageFilter
import numpy as np
import os
from datetime import datetime

def analyze_image(file):
    try:
        img = Image.open(file.name)
        analysis = {
            'size': img.size,
            'format': img.format,
            'mode': img.mode,
        }

        # Color analysis
        img_small = img.resize((50, 50))
        pixels = np.array(img_small)
        if len(pixels.shape) == 3:
            dominant_rgb = tuple(np.mean(pixels.reshape(-1, 3), axis=0).astype(int))
            analysis['dominant_color'] = f"RGB: {dominant_rgb}, Hex: #{dominant_rgb[0]:02x}{dominant_rgb[1]:02x}{dominant_rgb[2]:02x}"
        else:
            gray_val = int(np.mean(pixels))
            analysis['dominant_color'] = f"RGB: ({gray_val}, {gray_val}, {gray_val})"

        # Edge detection
        edges = img.filter(ImageFilter.FIND_EDGES)
        return edges, analysis

    except Exception as e:
        return None, f"Error: {str(e)}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# AI Image Analyzer")
    with gr.Row():
        input_image = gr.File(label="Upload Image")
        analyze_btn = gr.Button("Analyze")
    with gr.Row():
        output_image = gr.Image(label="Edge Detection")
        output_text = gr.JSON(label="Analysis Results")

    analyze_btn.click(
        fn=analyze_image,
        inputs=input_image,
        outputs=[output_image, output_text]
    )

demo.launch()