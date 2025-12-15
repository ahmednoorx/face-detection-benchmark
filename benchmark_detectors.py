"""
Face detection benchmark: MediaPipe vs MTCNN vs InsightFace (RetinaFace/SCRFD)

- Reads images from `benchmark_images/`
- Measures detection count and per-image latency
- Saves `BENCHMARK_RESULTS.md`
- Writes annotated examples to `benchmark_outputs/`

Optional GPU (Colab/Kaggle): change providers for InsightFace to `CUDAExecutionProvider`.
"""
from __future__ import annotations
import time
from pathlib import Path
from typing import List, Tuple
import cv2
import numpy as np

# Lazy imports with helpful errors

def _import_mediapipe():
    try:
        import mediapipe as mp  # type: ignore
        return mp
    except Exception as e:
        raise RuntimeError("Install mediapipe: pip install mediapipe") from e

def _import_mtcnn():
    try:
        from mtcnn import MTCNN  # type: ignore
        return MTCNN
    except Exception as e:
        raise RuntimeError("Install mtcnn: pip install mtcnn") from e

def _import_insightface():
    try:
        from insightface.app import FaceAnalysis  # type: ignore
        return FaceAnalysis
    except Exception as e:
        raise RuntimeError("Install insightface: pip install insightface onnxruntime") from e


def list_images(img_dir: Path) -> List[Path]:
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".avif", ".webp"}
    return [p for p in sorted(img_dir.glob("**/*")) if p.suffix.lower() in exts]


def draw_box(img: np.ndarray, box: Tuple[int,int,int,int], color=(0,255,0), text: str|None=None):
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    if text:
        cv2.putText(img, text, (x1, max(10, y1-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)


def annotate_and_save(detector_name: str, img_path: Path, boxes: List[Tuple[int,int,int,int]], out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    img = cv2.imread(str(img_path))
    if img is None:
        return
    for i, b in enumerate(boxes):
        draw_box(img, b, (0,255,0), f"{detector_name}")
    out_path = out_dir / f"{img_path.stem}_{detector_name}.jpg"
    cv2.imwrite(str(out_path), img)


# Benchmarks

def benchmark_mtcnn(img_paths: List[Path]):
    MTCNN = _import_mtcnn()
    detector = MTCNN()
    results = []
    for p in img_paths:
        img = cv2.imread(str(p))
        if img is None:
            continue
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        t0 = time.time()
        faces = detector.detect_faces(rgb) or []
        elapsed = time.time() - t0
        boxes = []
        for f in faces:
            x, y, w, h = f.get('box', [0,0,0,0])
            boxes.append((x, y, x+w, y+h))
        results.append((p.name, len(boxes), elapsed, boxes))
    return results


def benchmark_mediapipe(img_paths: List[Path]):
    mp = _import_mediapipe()
    detector = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)
    results = []
    for p in img_paths:
        img = cv2.imread(str(p))
        if img is None:
            continue
        h, w = img.shape[:2]
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        t0 = time.time()
        res = detector.process(rgb)
        elapsed = time.time() - t0
        boxes = []
        if res.detections:
            for d in res.detections:
                bb = d.location_data.relative_bounding_box
                x1 = int(bb.xmin * w)
                y1 = int(bb.ymin * h)
                x2 = int((bb.xmin + bb.width) * w)
                y2 = int((bb.ymin + bb.height) * h)
                boxes.append((x1, y1, x2, y2))
        results.append((p.name, len(boxes), elapsed, boxes))
    return results


def benchmark_insightface(img_paths: List[Path], providers=None):
    if providers is None:
        providers = ['CPUExecutionProvider']
    FaceAnalysis = _import_insightface()
    app = FaceAnalysis(providers=providers)
    app.prepare(ctx_id=0, det_size=(640, 640))
    results = []
    for p in img_paths:
        img = cv2.imread(str(p))
        if img is None:
            continue
        t0 = time.time()
        faces = app.get(img) or []
        elapsed = time.time() - t0
        boxes = []
        for f in faces:
            x1, y1, x2, y2 = f.bbox.astype(int).tolist()
            boxes.append((x1, y1, x2, y2))
        results.append((p.name, len(boxes), elapsed, boxes))
    return results


def write_report(img_paths: List[Path], mtcnn_res, mp_res, inf_res, out_file: Path):
    idx = {p.name: i for i, p in enumerate(img_paths)}
    # Align by image name
    with out_file.open('w', encoding='utf-8') as f:
        f.write('# Detection Pipeline Benchmark\n\n')
        f.write('| Image | MTCNN | MediaPipe | InsightFace |\n')
        f.write('|-------|-------|-----------|-------------|\n')
        for p in img_paths:
            name = p.name
            mt = next((r for r in mtcnn_res if r[0]==name), None)
            mp = next((r for r in mp_res if r[0]==name), None)
            inf = next((r for r in inf_res if r[0]==name), None)
            mt_s = f"{mt[1]} ({mt[2]:.2f}s)" if mt else '—'
            mp_s = f"{mp[1]} ({mp[2]:.2f}s)" if mp else '—'
            inf_s = f"{inf[1]} ({inf[2]:.2f}s)" if inf else '—'
            f.write(f"| {name} | {mt_s} | {mp_s} | {inf_s} |\n")


def main():
    img_dir = Path('benchmark_images')
    out_anno = Path('benchmark_outputs')
    out_report = Path('BENCHMARK_RESULTS.md')

    imgs = list_images(img_dir)
    if not imgs:
        print('No images found in benchmark_images/. Run download_benchmark_images.py or add images.')
        return

    print(f"Found {len(imgs)} images. Running benchmarks...\n")

    # Skip MTCNN (requires TensorFlow); compare MediaPipe vs InsightFace
    mtcnn = []
    print('[SKIP] MTCNN (requires TensorFlow)\n')

    print('=== MediaPipe ===')
    mp = benchmark_mediapipe(imgs)
    for name, count, t, boxes in mp:
        print(f"{name}: {count} faces, {t:.3f}s")
    for r in mp:
        annotate_and_save('MediaPipe', img_dir / r[0], r[3], out_anno)

    print('\n=== InsightFace ===')
    inf = benchmark_insightface(imgs, providers=['CPUExecutionProvider'])
    for name, count, t, boxes in inf:
        print(f"{name}: {count} faces, {t:.3f}s")
    for r in inf:
        annotate_and_save('InsightFace', img_dir / r[0], r[3], out_anno)

    write_report(imgs, mtcnn, mp, inf, out_report)
    print(f"\n[OK] Report saved to {out_report.resolve()}")
    print(f"[OK] Annotated samples saved to {out_anno.resolve()}")


if __name__ == '__main__':
    main()
