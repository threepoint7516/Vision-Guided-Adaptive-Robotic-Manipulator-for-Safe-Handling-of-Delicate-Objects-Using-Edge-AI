# pi/

Python that runs on the Raspberry Pi 5 (Track C).

Planned modules in `src/arm/`:

- `serial_link.py` - protocol to the STM32 (set joint angle, read status, gripper, stop)
- `kinematics.py` - own FK/IK, checked against roboticstoolbox
- `vision.py` - camera capture, calibration, YOLO11n NCNN detector, colour/shape fallback
- `logger.py` - CSV run logs into `data/logs/`

Setup: see the root README.
