# Vision-Guided Adaptive Robotic Manipulator for Safe Handling of Delicate Objects Using Edge AI

Final year project. A 6-axis arm with a force-limited soft-pad gripper that detects eggs with a camera and handles them without cracking, with AI running on a Raspberry Pi 5.

- **FYP-I (12 weeks):** arm built and moving from Python, gripper that stops at a force limit, e-stop, camera calibration, egg detector running live on the Pi. Tests use foam, ping-pong balls and an egg-shaped dummy.
- **FYP-II:** autonomous real-egg pick and place (80%+ success, zero cracks, placement within 20 mm).

Spec: [docs/requirements-spec.md](docs/requirements-spec.md) (supervisor approved, Oct 24, 2026).

## Layout

| Folder | What goes there | Track |
| --- | --- | --- |
| `firmware/` | STM32 Nucleo-F446RE firmware (STM32CubeIDE + HAL) | B |
| `pi/` | Raspberry Pi 5 Python: vision, serial link, kinematics, logging | C |
| `cad/` | CAD models, drawings, STL/STEP exports | A |
| `docs/` | Spec, BOM, torque calcs, test reports, FYP report drafts | all |
| `data/logs/` | Small run logs (CSV). Big datasets stay out of Git | C |

Datasets and trained weights live on Roboflow / Google Drive, not in Git.

## Hardware

Steppers with low-backlash gearboxes on J1 to J4 (NEMA23 on J2), DS3218 servos on J5 and J6, AS5600 encoders on J1 to J3, TMC2209 + DM542 drivers on 24 V, STS3215 gripper servo, 1 kg load cell + HX711, Logitech C920 overhead, Raspberry Pi 5 8 GB. Full table in the spec.

## Pi setup

On Raspberry Pi OS 64-bit (Python 3.11+):

```bash
cd pi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements-dev.txt` adds roboticstoolbox-python for checking our own FK/IK on a laptop.

## Firmware setup

Open STM32CubeIDE, create the project for NUCLEO-F446RE inside `firmware/` (see [firmware/README.md](firmware/README.md)).

## Task board

One GitHub issue per roadmap task, labelled `track:A`, `track:B` or `track:C` and `week-N`. Work on a branch and open a PR to `main`.
