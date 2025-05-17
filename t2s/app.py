from flask import Flask, render_template, request, jsonify, send_file
import os
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import cv2
import numpy as np

app = Flask(__name__)

# Initialize the model pipeline
pipe = DiffusionPipeline.from_pretrained(
    "damo-vilab/text-to-video-ms-1.7b",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

@app.route('/')
def index():
    return render_template('ttindex.html')

@app.route('/generate-video', methods=['POST'])
def generate_video():
    prompt = request.json.get('prompt')
    
    num_inference_steps = 200
    video_frames = pipe(prompt, num_inference_steps=num_inference_steps).frames

    if len(video_frames[0].shape) == 4:
        video_frames = [frame for batch in video_frames for frame in batch]

    target_resolution = (1920, 1080)
    fps = 30
    duration = 10
    total_frames = duration * fps

    if len(video_frames) < total_frames:
        video_frames = video_frames * (total_frames // len(video_frames))
        video_frames = video_frames[:total_frames]

    output_video_path = os.path.join('pooj', 'output_video.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, target_resolution)

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    for frame in video_frames:
        frame = np.array(frame)
        if len(frame.shape) == 3 and frame.shape[2] == 3:
            frame = cv2.filter2D(frame, -1, kernel)
            if frame.dtype != np.uint8:
                frame = cv2.convertScaleAbs(frame, alpha=(255.0 / frame.max()))
            frame = cv2.resize(frame, target_resolution, interpolation=cv2.INTER_CUBIC)
            video_writer.write(frame)

    video_writer.release()
    
    return jsonify({'video_url': '/download-video'})

@app.route('/download-video')
def download_video():
    return send_file(os.path.join('pooj', 'output_video.mp4'), as_attachment=True)

if __name__ == '_main_':
    app.run(debug=True)