# Joint torque calculations (Week 2, draft)

Links (locked 2026-10-27): upper arm 20 cm, forearm 17 cm, wrist + gripper 8 cm (45 cm reach from J2 axis).
Worst case: arm horizontal and fully extended, 250 g payload, J3 motor + gearbox at the elbow.
Masses are estimates; re-check against CAD masses in Week 3. Safety margin 50% (roadmap asks 30-50%).

## Assumed masses

| Item | Mass (kg) | Distance from J2 (m) |
|---|---|---|
| Payload | 0.25 | 0.45 |
| Gripper (STS3215, load cell, fingers) | 0.20 | 0.41 |
| Wrist (2x DS3218 + brackets) | 0.17 | 0.37 |
| J4 short NEMA17 + gearbox | 0.25 | 0.24 |
| J3 NEMA17 + 15:1 gearbox | 0.55 | 0.20 |
| Forearm link | 0.15 | 0.285 |
| Upper arm link | 0.20 | 0.10 |

## Results

| Joint | Load case | Static (N·m) | With 50% margin (N·m) | Actuator available (N·m) | OK |
|---|---|---|---|---|---|
| J1 base yaw | inertia 0.16 kg·m², 0-90°/s in 0.3 s, + friction | ~0.9 | ~1.3 | NEMA17 0.45 x 10:1 x 0.9 = ~4.0 | Yes |
| J2 shoulder | gravity, arm extended | 4.8 | 7.2 | NEMA23 1.2 x 10:1 x 0.9 = ~10.8 | Yes (1.5x) |
| J3 elbow | gravity, forearm extended | 1.53 | 2.3 | NEMA17 0.45 x 15:1 x 0.9 = ~6.0 | Yes |
| J4 forearm roll | payload + gripper 8 cm off-axis (wrist bent 90°) | 0.35 | 0.53 | short NEMA17 ~0.25 direct: **too low**; with 5:1 gearbox ~1.1 | Needs 5:1 |
| J5 wrist pitch | payload + gripper | 0.27 | 0.41 | DS3218 ~1.9 at 6 V | Yes |
| J6 wrist roll | gripper off-axis only | <0.1 | <0.15 | DS3218 ~1.9 at 6 V | Yes |

Gearbox efficiency taken as 0.9. Stepper torque falls with speed, so keep J2/J3 moves slow (under ~300 rpm motor side) or re-check against the motor's pull-out curve once a model is picked.

## Notes
- J4 must use a planetary gearbox (5:1 low-backlash) — the short NEMA17 alone can't hold the wrist-bent case.
- J3 at 15:1 has 2.6x margin; 10:1 would also pass (~4 N·m) and is faster. Keep 15:1 for resolution unless speed is an issue.
- FYP-II: same payload and reach, so these numbers carry over.
