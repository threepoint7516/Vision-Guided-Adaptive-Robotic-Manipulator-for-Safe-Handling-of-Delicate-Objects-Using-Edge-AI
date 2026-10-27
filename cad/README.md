# cad/

Mechanical design (Track A): base, links, wrist, gripper, camera mount. Keep source files plus STEP/STL exports and drawings (PDF). Large renders and videos go to Google Drive.

## Week 2 draft (CadQuery)

`arm_draft.py` builds a parametric first pass of the arm in the zero pose (DH frame, see `docs/dh-parameters.md`):
base (J1 NEMA17 + 10:1 under the turntable, 51110 thrust bearing), shoulder uprights (J2 NEMA23 + 10:1, 6806 bearing, counterbalance spring lug), upper arm (twin plates, 200 mm), forearm (J3 elbow block, J4 short NEMA17 + 5:1, 170 mm to wrist centre), wrist (J5/J6 DS3218 brackets) and a gripper concept (STS3215 pinion + two racks, parallel fingers, load cell in one finger, 3 mm silicone pads, 0-70 mm opening).

```
pip install cadquery
python cad/arm_draft.py      # writes cad/out/*.step, *.stl, arm_assembly.step
```

Open `cad/out/arm_assembly.step` in Fusion 360 to refine. Change dimensions at the top of the script, not in the STEP.
Printed-mass estimates it prints (PETG, ~40% fill) are below the torque-calc assumptions, so the torque margins hold. Servo/motor bodies in wrist and gripper are placeholders, not printed parts.

Before CAD freeze (Week 3): measure the real gearbox flanges and shafts, add couplings and set screws, cable paths, limit-switch flags, and the J2 spring size.
