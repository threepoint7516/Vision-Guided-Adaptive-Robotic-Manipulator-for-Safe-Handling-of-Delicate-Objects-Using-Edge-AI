"""Week 2 draft CAD for the arm (CadQuery).

Parametric first pass: base, shoulder, upper arm, forearm, wrist and gripper
concept. Dimensions follow docs/dh-parameters.md and docs/torque-calcs.md.
Run:  python cad/arm_draft.py   ->  writes STEP + STL to cad/out/
Refine in Fusion 360 from the STEP files; keep the numbers below in sync.
"""
from pathlib import Path

import cadquery as cq

# --- locked dimensions (mm) ---
D1 = 150.0   # J2 axis height above table
A2 = 200.0   # upper arm, J2 to J3
D4 = 170.0   # forearm, J3 to wrist centre
D6 = 80.0    # wrist centre to gripper tip

# --- actuator interfaces (check against the parts that arrive) ---
NEMA17 = 42.3
NEMA17_HOLES = 31.0
NEMA17_PILOT = 22.0
NEMA23 = 57.0
GBX23_FLANGE = 60.0       # NEMA23 planetary output flange (square)
GBX23_BOLT_PCD = 70.0
GBX17_FLANGE = 42.0       # NEMA17 planetary output flange (square)
DS3218 = (40.0, 20.0, 40.5)  # body L x W x H
DS3218_TAB = 54.0         # mounting tab span
STS3215 = (45.2, 24.7, 35.0)

# --- structure ---
WALL = 5.0
LINK_W = 60.0
LINK_T = 8.0              # side-plate thickness
BEARING_6806 = (42.0, 7.0)  # OD, width: J2/J3 output-side support
THRUST_51110 = (70.0, 16.0)  # J1 thrust bearing OD, height

OUT = Path(__file__).parent / "out"


def base():
    """Fixed base: plate, J1 motor (NEMA17 + 10:1 gearbox) hanging below the turntable."""
    plate = cq.Workplane("XY").rect(180, 180).extrude(8).edges("|Z").fillet(10)
    plate = plate.faces(">Z").workplane().rect(160, 160, forConstruction=True).vertices().hole(6)
    tower = (cq.Workplane("XY").workplane(offset=8)
             .circle(55).circle(55 - WALL).extrude(60))
    top = (cq.Workplane("XY").workplane(offset=68).circle(55).extrude(6)
           .faces(">Z").workplane().hole(THRUST_51110[0] - 20)
           .faces(">Z").workplane().circle(THRUST_51110[0] / 2).cutBlind(-3))
    motor_mount = (cq.Workplane("XY").workplane(offset=68 - 6)
                   .rect(NEMA17 + 10, NEMA17 + 10).extrude(6)
                   .faces(">Z").workplane().hole(NEMA17_PILOT + 1)
                   .faces(">Z").workplane().rect(NEMA17_HOLES, NEMA17_HOLES, forConstruction=True)
                   .vertices().hole(3.4))
    return plate.union(tower).union(top).union(motor_mount)


def shoulder():
    """Turntable + two uprights carrying the J2 NEMA23 geared motor; J2 axis at D1."""
    z0 = 74.0  # top of base
    turntable = cq.Workplane("XY").workplane(offset=z0).circle(60).extrude(8)
    gap = LINK_W + 2
    upright_h = D1 - z0 + 35
    left = (cq.Workplane("XY").workplane(offset=z0 + 8)
            .center(0, gap / 2 + LINK_T / 2).rect(80, LINK_T).extrude(upright_h - 8))
    right = left.mirror("XZ")
    # J2 holes: gearbox flange side (+y) and 6806 bearing side (-y)
    bore = (cq.Workplane("XZ").workplane(offset=-(gap / 2 + LINK_T + 1))
            .center(0, D1).circle(GBX23_FLANGE / 2 * 0.6).extrude(gap + 2 * LINK_T + 2))
    brg = (cq.Workplane("XZ").workplane(offset=gap / 2 - 1)
           .center(0, D1).circle(BEARING_6806[0] / 2).extrude(LINK_T + 2))
    spring_lug = (cq.Workplane("XY").workplane(offset=z0 + 8)
                  .center(-50, 0).rect(12, gap).extrude(30)
                  .faces(">Z").workplane().center(0, 0).hole(5))  # J2 counterbalance spring anchor
    body = turntable.union(left).union(right).union(spring_lug).cut(bore).cut(brg)
    return body


def upper_arm():
    """Two side plates joined by spacers, J2 hub at origin, J3 hub at A2 (along +x, zero pose)."""
    def plate(y):
        p = (cq.Workplane("XZ").workplane(offset=y)
             .center(A2 / 2, 0).slot2D(A2 + 50, 50).extrude(LINK_T)
             .faces("<Y").workplane().pushPoints([(-A2 / 2, 0), (A2 / 2, 0)]).hole(22)
             .faces("<Y").workplane().center(0, 0).slot2D(A2 - 80, 20).cutThruAll())
        return p
    side = plate(-LINK_W / 2).union(plate(LINK_W / 2 + LINK_T))
    spacers = (cq.Workplane("XZ").workplane(offset=-LINK_W / 2 - LINK_T)
               .pushPoints([(60, 0), (A2 - 60, 0)]).rect(12, 30).extrude(LINK_W + LINK_T * 2))
    arm = side.union(spacers)
    return arm.translate((0, 0, D1))


def forearm():
    """Elbow block holding J3 NEMA17 + 15:1, forearm tube with J4 short NEMA17 + 5:1 at the elbow end."""
    elbow = (cq.Workplane("XY").box(70, LINK_W - 2, 60)
             .faces("+Y").workplane().hole(GBX17_FLANGE / 2))
    tube = (cq.Workplane("YZ").workplane(offset=35)
            .circle(28).circle(28 - WALL).extrude(D4 - 35 - 30))
    j4_mount = (cq.Workplane("YZ").workplane(offset=35)
                .rect(NEMA17 + 8, NEMA17 + 8).extrude(5)
                .faces(">X").workplane().rect(NEMA17_HOLES, NEMA17_HOLES, forConstruction=True)
                .vertices().hole(3.4))
    return elbow.union(tube).union(j4_mount).translate((A2, 0, D1))


def wrist():
    """J4 output disc, U-bracket for J5 DS3218 (pitch), J6 DS3218 (roll) at the wrist centre."""
    x_wc = A2 + D4
    disc = cq.Workplane("YZ").workplane(offset=x_wc - 30).circle(28).extrude(6).translate((0, 0, D1))
    l, w, h = DS3218
    j5_body = cq.Workplane("XY").box(h, w, l).translate((x_wc - 10, 0, D1))
    j5_tabs = cq.Workplane("XY").box(h, w, 3).translate((x_wc - 10, 0, D1 + DS3218_TAB / 2 - 10))
    ubracket = (cq.Workplane("XY").box(50, w + 2 * 4 + 6, 4).translate((x_wc + 5, 0, D1 - 25))
                .union(cq.Workplane("XY").box(4, w + 2 * 4 + 6, 50).translate((x_wc + 28, 0, D1))))
    j6_body = cq.Workplane("XY").box(l, w, h).translate((x_wc + 30 + h / 2, 0, D1))
    return disc.union(j5_body).union(j5_tabs).union(ubracket).union(j6_body)


def gripper():
    """Concept: STS3215 drives a pinion between two racks -> parallel fingers.
    Finger A carries the 1 kg bar load cell; both have 3 mm silicone pads. Opening 0-70 mm."""
    x0 = A2 + D4 + 50
    palm = cq.Workplane("XY").box(20, 90, 40).translate((x0, 0, D1))
    servo = cq.Workplane("XY").box(STS3215[2], STS3215[1], STS3215[0]).translate((x0 - 22, 0, D1))
    rail = cq.Workplane("XY").box(10, 110, 10).translate((x0 + 12, 0, D1 + 12))
    finger_len = D6 - 50 + 10
    fa = (cq.Workplane("XY").box(finger_len, 8, 30).translate((x0 + 10 + finger_len / 2, 25, D1)))
    load_cell = cq.Workplane("XY").box(55, 12.7, 12.7).translate((x0 + 10 + 27, 25 + 11, D1 + 20))
    fb = fa.mirror("XZ", basePointVector=(0, 0, 0))
    pads = (cq.Workplane("XY").box(25, 3, 25).translate((x0 + 10 + finger_len - 12.5, 25 - 5.5, D1))
            .union(cq.Workplane("XY").box(25, 3, 25).translate((x0 + 10 + finger_len - 12.5, -25 + 5.5, D1))))
    return palm.union(servo).union(rail).union(fa).union(fb).union(load_cell).union(pads)


PARTS = {
    "base": base,
    "shoulder": shoulder,
    "upper_arm": upper_arm,
    "forearm": forearm,
    "wrist": wrist,
    "gripper_concept": gripper,
}


def main():
    OUT.mkdir(exist_ok=True)
    asm = cq.Assembly(name="arm_zero_pose")
    for name, fn in PARTS.items():
        shape = fn()
        cq.exporters.export(shape, str(OUT / f"{name}.step"))
        cq.exporters.export(shape, str(OUT / f"{name}.stl"))
        vol_cm3 = shape.val().Volume() / 1000
        # PETG 1.27 g/cm3 at ~40% effective fill (walls + infill)
        print(f"{name:16s} {vol_cm3:7.1f} cm3  ~{vol_cm3 * 1.27 * 0.4:6.0f} g printed")
        asm.add(shape, name=name)
    asm.save(str(OUT / "arm_assembly.step"))


if __name__ == "__main__":
    main()
