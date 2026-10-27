# DH parameters (Week 2, draft)

Standard (Denavit-Hartenberg) convention. Base frame on the table under J1, z up.
Locked dimensions: shoulder height d1 = 150 mm, upper arm a2 = 200 mm, forearm d4 = 170 mm, wrist centre to gripper tip d6 = 80 mm. J4-J6 axes meet at one point (spherical wrist), so IK splits into position (J1-J3) and orientation (J4-J6).

| i | Joint | θ_i | d_i (mm) | a_i (mm) | α_i |
|---|---|---|---|---|---|
| 1 | Base yaw | θ1 | 150 | 0 | +90° |
| 2 | Shoulder pitch | θ2 | 0 | 200 | 0° |
| 3 | Elbow pitch | θ3 + 90° | 0 | 0 | +90° |
| 4 | Forearm roll | θ4 | 170 | 0 | −90° |
| 5 | Wrist pitch | θ5 | 0 | 0 | +90° |
| 6 | Gripper roll | θ6 | 80 | 0 | 0° |

Zero pose (all θ = 0): arm straight and horizontal along +x, tool tip at (450, 0, 150) mm, tool z-axis along +x. Checked numerically.
Top-down grasp: θ5 = −90° from the zero pose puts the tool pointing down; tip at (370, 0, 70) mm.

Joint limits (draft, refine with CAD): J1 ±170°, J2 −10°..+120°, J3 −135°..+90°, J4 ±170°, J5 ±100° (servo 270° range), J6 ±135°.

FK check in Python:
```python
import numpy as np
def T(th, d, a, al):
    c, s, ca, sa = np.cos(th), np.sin(th), np.cos(al), np.sin(al)
    return np.array([[c,-s*ca,s*sa,a*c],[s,c*ca,-c*sa,a*s],[0,sa,ca,d],[0,0,0,1]])
```
To be cross-checked against roboticstoolbox (DHRobot) when pi/ code starts. Update d/a values from the CAD once frozen in Week 3.
