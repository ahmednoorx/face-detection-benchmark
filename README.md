# Face Detection Benchmark (MediaPipe vs InsightFace)

A reproducible benchmark comparing MediaPipe, MTCNN, and InsightFace on a 30-image real-world set. Includes CPU and Colab GPU runs, annotated outputs, and a clear speed/accuracy trade-off story you can hand to stakeholders.

## What’s inside
- `benchmark_detectors.py` — main runner for CPU benchmarks on the local image set.
- `BENCHMARK_RESULTS.md` — per-image table plus summary stats and GPU callout.
- `BENCHMARK_README.md` — detailed quick start and supervisor talking points.
- `GPU_Benchmark_Colab.ipynb` — Colab notebook to rerun InsightFace on GPU with the exact same images.
- `benchmark_outputs/` — annotated detections (MediaPipe + InsightFace) for visual proof.
- `benchmark_images/` — the 30-image input set used for the reported numbers.

## Headline results
- MediaPipe (CPU): ~125 FPS, detected 28/30 images (missed 2 profile/low-light cases).
- InsightFace (CPU): 2.6 FPS, detected 30/30 images, caught extra faces in multi-person shots.
- InsightFace (GPU, T4): 5.8 FPS (0.172s/image), **2.2× faster** vs CPU while keeping 100% recall.

## How to reproduce (CPU)
```powershell
conda create -n vision-bench python=3.11 -y
conda activate vision-bench
pip install mediapipe mtcnn insightface onnxruntime opencv-python numpy
python benchmark_detectors.py
```
Outputs: `BENCHMARK_RESULTS.md` and annotated images in `benchmark_outputs/`.

## How to reproduce (GPU on Colab/Kaggle)
1) Zip your `benchmark_images/` as `benchmark_images.zip` and upload when prompted.
2) Open `GPU_Benchmark_Colab.ipynb`, set runtime to GPU (T4/P100/V100).
3) Run all cells; the notebook reuses the uploaded images so CPU vs GPU is apples-to-apples.

## Data and sharing
- Images are real photos (no synthetic). If publishing publicly, keep only a small CC0 sample and add a note that the full set is held privately for privacy/licensing.
- Annotated outputs are in `benchmark_outputs/` (60 images total: 30 MediaPipe + 30 InsightFace).

## Suggested repo structure for GitHub
- Keep this root `README.md` plus the two benchmark markdowns, scripts, and the Colab notebook.
- Include a **small sample** of `benchmark_images/` (e.g., 5 CC0 photos) and note that the full set is private; optionally omit `benchmark_outputs/` or keep a few samples to reduce repo size.
- Add a short cover note in your PR/commit message with the headline numbers and the key surprise: InsightFace catching the second face in `8.jpg`.

## Quick talking points
- Speed vs accuracy: MediaPipe for real-time light use; InsightFace for maximum recall (GPU recommended) or a hybrid pipeline.
- Auditability: Every detection is visually reviewable via `benchmark_outputs/`.
- GPU story: Moving InsightFace to a modest T4 roughly halves latency while keeping accuracy identical.
