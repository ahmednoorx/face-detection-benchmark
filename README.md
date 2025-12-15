# Face Detection Benchmark: MediaPipe vs InsightFace

A systematic performance comparison of MediaPipe and InsightFace face detection models on a 30-image dataset. This project evaluates detection accuracy, speed, and GPU acceleration to guide model selection for real-world applications.

## Overview
Face detection is critical for applications ranging from security systems to photo management. This benchmark compares two leading detectors:
- **MediaPipe**: Google's lightweight, real-time solution
- **InsightFace**: Deep learning-based detector optimized for accuracy

The evaluation uses 30 real-world images with diverse conditions (lighting, angles, occlusions, group photos) and measures both CPU and GPU performance.

## Repository Contents
- `benchmark_detectors.py` — Main script to run CPU benchmarks
- `GPU_Benchmark_Colab.ipynb` — Colab notebook for GPU evaluation (T4/P100/V100)
- `BENCHMARK_RESULTS.md` — Detailed per-image results table with timing and detection counts
- `BENCHMARK_README.md` — Setup instructions and methodology

## Key Findings

### CPU Performance
| Detector | Images Detected | Avg FPS | Total Faces Found |
|----------|----------------|---------|-------------------|
| MediaPipe | 28/30 (93%) | 125 | 29 |
| InsightFace | 30/30 (100%) | 2.6 | 32 |

**MediaPipe** excels at speed (~125 FPS) but missed 2 images with challenging conditions (profile angles, low light).

**InsightFace** achieved 100% image detection and identified all faces in multi-person scenes, including cases MediaPipe missed, at the cost of slower processing (2.6 FPS on CPU).

### GPU Acceleration
Running InsightFace on a **T4 GPU** delivered:
- **5.8 FPS** (0.172s per image)
- **2.2× speedup** over CPU (0.378s → 0.172s)
- Same 100% detection accuracy maintained

## Methodology
1. **Dataset**: 30 diverse real-world images (frontal, profile, groups, occlusions)
2. **Environment**: Python 3.11, OpenCV, tested on CPU (local) and T4 GPU (Google Colab)
3. **Metrics**: Detection rate (images with ≥1 face found), face count, per-image latency
4. **Reproducibility**: Same image set used for CPU and GPU runs to ensure fair comparison

## Setup & Reproduction
```bash
# Create environment
conda create -n vision-bench python=3.11 -y
conda activate vision-bench
pip install mediapipe insightface onnxruntime opencv-python numpy

# Run CPU benchmark
python benchmark_detectors.py
```

For GPU evaluation, open `GPU_Benchmark_Colab.ipynb` in Google Colab and follow the notebook instructions.

## Recommendations
- **Real-time applications** (webcams, mobile): MediaPipe for speed
- **High-accuracy needs** (security, analytics): InsightFace with GPU acceleration
- **Hybrid approach**: MediaPipe for initial scan, InsightFace for verification

## License
MIT License - see individual library licenses for MediaPipe and InsightFace.
