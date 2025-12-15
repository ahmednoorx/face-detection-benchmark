# Face Detection Benchmark – Quick Start

This folder contains everything to benchmark MediaPipe, MTCNN, and InsightFace detectors on a small image set.

## 1) Create a separate environment (don’t use `llm101`)

```powershell
conda create -n vision-bench python=3.11 -y
conda activate vision-bench
pip install mediapipe mtcnn insightface onnxruntime opencv-python numpy
```

If you later use Colab/Kaggle GPU for InsightFace:
```bash
pip install insightface onnxruntime-gpu
```

## 2) Get images

Option A (scripted seed set):
- Run `python download_benchmark_images.py` to grab a starter pack of CC0 photos.
- Manually review and replace anything that is low quality or synthetic.

Option B (recommended for final runs):
- Collect at least **30 real photos** (same ones you plan to show your supervisor) and place them in `benchmark_images/`.
- Include frontal, profile, groups, occlusions (masks/sunglasses), low light, multiple ethnicities.
- When you need to benchmark on Colab, zip this exact folder as `benchmark_images.zip` so CPU and GPU runs use identical inputs.

## 3) Run the benchmark

```powershell
python benchmark_detectors.py
```
Outputs:
- `BENCHMARK_RESULTS.md` — table with counts and latency per detector
- `benchmark_outputs/` — annotated example images (boxes/landmarks)

## 4) Optional: GPU run on Colab/Kaggle
- Zip `benchmark_images/` → `benchmark_images.zip` and upload it when the notebook prompts.
- Open `GPU_Benchmark_Colab.ipynb` in Colab, switch runtime to GPU (T4/P100/V100).
- Run every cell in order. The notebook now loads the uploaded zip and reuses the exact same images from the CPU test, so comparisons are apples-to-apples.

## Supervisor Talking Points
1. **Speed vs Accuracy Trade-off** – MediaPipe hits ~125 FPS but missed 2/30 images; InsightFace is slower on CPU (2.6 FPS) but delivered 100% recall and caught extra faces in multi-person shots.
2. **Audit Trail** – All 30 images now have MediaPipe + InsightFace annotations in `benchmark_outputs/`, so every detection (or miss) can be visually verified.
3. **GPU Story** – The Colab notebook uploads the exact same dataset, proving InsightFace jumps from 0.378s/image on CPU (2.6 FPS) to **0.172s/image on a T4 GPU (5.8 FPS, 2.2× faster)**. Recommendation: GPU for surveillance/mission-critical accuracy, MediaPipe for lightweight real-time use, or a hybrid pipeline.
4. **Personal notes** – I kept the same 30-photo set for CPU and GPU so the comparison is defensible; biggest surprise was InsightFace catching the second subject in `8.jpg` that MediaPipe missed.
## Notes
- If MediaPipe import fails on Windows, upgrade: `pip install --upgrade mediapipe`.
- If InsightFace fails on CPU due to ONNX providers, ensure `onnxruntime` is installed and selected.
