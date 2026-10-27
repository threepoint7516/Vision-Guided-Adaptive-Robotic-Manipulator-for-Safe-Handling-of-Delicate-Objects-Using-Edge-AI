# Power budget, wiring plan and e-stop (Week 2, draft)

## Power budget

| Rail | Source | Loads | Worst-case draw | Supply rating |
|---|---|---|---|---|
| 24 V motor | 24 V 10 A (240 W) SMPS | J1, J3, J4 NEMA17 on TMC2209 (~1.0 A each from supply); J2 NEMA23 on DM542 (~2 A) | ~5 A | 10 A (2x margin) |
| 6 V servo | 24 V -> 6 V 20 A buck (from motor rail) | 2x DS3218 (2.5 A stall each), STS3215 (~2 A stall) | ~7 A stall, ~2 A typical | 20 A |
| 5 V Pi | Official Pi 5 27 W USB-C supply (own mains plug) | Pi 5 + C920 + Nucleo over USB | ~4 A | 5 A |
| 3.3 V logic | Nucleo on-board regulator | AS5600 x3, HX711, e-stop sense | <0.1 A | — |

Motor current from the supply is below phase current because the drivers chop at 24 V; numbers are worst case with all joints holding.

## Wiring plan

- Mains -> fused IEC inlet with switch -> 24 V SMPS.
- 24 V SMPS -> e-stop relay contact -> 24 V bus (fuse 8 A) -> 4 stepper drivers and the 6 V buck (fuse 10 A on the buck output).
- Pi 5 on its own supply, so an e-stop never reboots the Pi. Nucleo powered by USB from the Pi (also the serial link).
- Common ground: 24 V negative, 6 V negative, Nucleo GND tied at one star point.
- Signals: STM32 step/dir/enable to TMC2209 (UART for current set) and DM542 (opto inputs); PWM to DS3218s; half-duplex UART to STS3215; I2C to AS5600s (via TCA9548A mux, all have the same address); HX711 2-wire; limit switches on GPIO with pull-ups.
- Wire: 18 AWG for 24 V bus and servo power, 22-24 AWG shielded for encoder/load cell, drag-chain style routing along links.

## E-stop (locked 2026-10-27: hard cut + J2 spring)

- Red latching mushroom e-stop, 2 NC contacts.
- Contact 1 in series with the coil of a 24 V relay/contactor (rated 10 A DC); the relay contact feeds the whole 24 V bus, so both motor rails drop when pressed or if a wire breaks (fail-safe).
- Contact 2 to an STM32 GPIO (pull-up, interrupt): firmware latches a fault, stops step generation, and needs a manual reset command before moving again.
- Reset: twist-release the button, then a green "power on" push-button re-latches the relay (no auto-restart).
- J2 spring counterbalance (extension spring or gas spring, sized in CAD for ~50-70% of the arm's gravity torque) so the arm sinks slowly when motor power drops. Also lowers J2 running load.
- Fits FYP-II: the watchdog safe stop can use the same relay path (STM32 GPIO can open the relay coil loop).
