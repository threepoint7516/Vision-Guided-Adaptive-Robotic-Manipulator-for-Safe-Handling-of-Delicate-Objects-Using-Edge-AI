# Costed BOM (Week 2)

Full list: [bom.csv](bom.csv). Prices are PKR estimates (USD ~280 PKR, China parts include ~25% shipping + customs); replace with real quotes as items are bought.

Budget: 240,000 PKR for FYP-I **and** FYP-II.

| Block | PKR |
|---|---|
| FYP-I parts (bom.csv) | ~210,000 |
| FYP-II reserve: ~150 eggs (~6,000), spare servos/parts (~12,000), pad materials, lighting, backdrop (~5,000), buffer (~7,000) | ~30,000 |
| **Total** | **~240,000** |

Not in budget: OAK-D Lite and Pi AI HAT+ (dropped; CPU YOLO11n on Pi 5 4 GB with the C920).

## Order this week (long lead, StepperOnline / AliExpress, ~82,000 + STS3215)
1. NEMA23 + 10:1 low-backlash (<=20 arcmin) planetary, J2
2. NEMA17 + 10:1 low-backlash planetary, J1
3. NEMA17 + 15:1 low-backlash planetary, J3
4. Short NEMA17 + 5:1 standard planetary, J4
5. DM542 driver
6. STS3215 bus servo (if not stocked locally)

Check before paying: shaft diameters match the planned couplings, motor rated current fits the drivers (TMC2209 <=2 A RMS, DM542 <=4.2 A), NEMA23 holding torque ~1.2 N·m or more.

Everything else is bought locally as Week 3 fabrication needs it.
