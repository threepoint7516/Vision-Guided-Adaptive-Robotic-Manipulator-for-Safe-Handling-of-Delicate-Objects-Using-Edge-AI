# firmware/

STM32 Nucleo-F446RE firmware (Track B), STM32CubeIDE + HAL.

Create the CubeIDE project here (e.g. `firmware/arm_controller/`). Commit the `.ioc`, `Core/`, `Drivers/` and project files; build folders are ignored.

Scope: step generation (TMC2209 x3, DM542 for J2), servo PWM (J5, J6), STS3215 gripper over UART, HX711 at 80 Hz, AS5600 on J1 to J3, limit switches, e-stop input, watchdog, serial command parser.
