# Sample Annotated Outputs

Representative examples from the benchmark showing detection results with bounding boxes and landmarks.

## Examples Included

### 1.jpg - Standard Single Face
- **MediaPipe**: Successfully detected
- **InsightFace**: Successfully detected

### 8.jpg - Multi-Person Detection
- **MediaPipe**: Detected 1 face (missed the second person)
- **InsightFace**: Detected 2 faces (found both subjects)
- **Key observation**: Demonstrates InsightFace's superior multi-face detection

### 11.jpg - Profile/Low-Light Challenge
- **MediaPipe**: 0 detections (missed)
- **InsightFace**: Successfully detected
- **Key observation**: One of the 2 cases where MediaPipe failed

### 20.jpg - Group Photo
- **MediaPipe**: Detected 2 faces
- **InsightFace**: Detected 2 faces
- **Key observation**: Both detectors handled this multi-person scene

## Notes
- Full set of 60 annotated images (30 × MediaPipe, 30 × InsightFace) available upon request
- Images show detection bounding boxes and facial landmarks overlaid on original photos
