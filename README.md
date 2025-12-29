
# PZEM-6L24 External Component for ESPHome

Support for three-phase PZEM-6L24 energy meters using Lucas Hudson  **lucashudson-eng/PZEMPlus** [PZEMPlus](https://github.com/lucashudson-eng/PZEMPlus) library.


## Tested with

- ESPHome 2025.11+
- ESP32-C3 
- PZEM-6L24 energy meter(s)
- MAX3485 / MAX485 RS-485 module
- lucashudson-eng/PZEMPlus library v0.73

## Supports
-   Multiple meters on one RS‑485 bus
-   Per‑phase **A / B / C** readings
-   Combined (3‑phase) totals
-   Hardware addressing support
-   Energy counter reset support

## Known Limitations / TODO
- Not all function's from Lucas his library are linked. 
- Calibration routine is not implemeted in PZEM library. 
- Using multiple sensors doing multiple readings will cause some time-outs. RS‑485 / Modbus polling is slow by nature.


## Directory Structure

```
energy-monitor.yaml
components/
  pzem6l24_plus/
    __init__.py
    sensor.py
    pzem6l24_plus.h
    pzem6l24_plus.cpp
```

## ESPHome‑Exposed Functions

These functions can be called directly from ESPHome lambdas, scripts,
buttons, or services.

### Addressing

``` cpp
id(pzem).use_hardware_address();
```

Uses hardware (DIP switch) addressing by calling:

    setAddress(0x00)

``` cpp
id(pzem).set_software_address(3);
```

Sets a software Modbus address (1‑247).

------------------------------------------------------------------------

### Energy Reset

``` cpp
id(pzem).reset_energy_all();
```

Resets **all energy counters** (A, B, C, and combined) using:

    resetEnergy(PZEM_RESET_ENERGY_ALL)

------------------------------------------------------------------------

## Supported Measurements See example yml.


### Per‑Phase (A / B / C)

  Function
  ------------------------------
  readVoltage(phase)
  readCurrent(phase)
  readFrequency(phase)
  readActivePower(phase)
  readReactivePower(phase)
  readApparentPower(phase)
  readPowerFactor(phase)
  readActiveEnergy(phase)
  readReactiveEnergy(phase)
  readApparentEnergy(phase)
  readVoltagePhaseAngle(phase)
  readCurrentPhaseAngle(phase)

Phase mapping: - `0` → Phase A - `1` → Phase B - `2` → Phase C

------------------------------------------------------------------------

### Combined (All Phases)

  Function
  ----------------------
  readActivePower()
  readReactivePower()
  readApparentPower()
  readPowerFactor()
  readActiveEnergy()
  readReactiveEnergy()
  readApparentEnergy()

------------------------------------------------------------------------

## ESPHome YAML Example

```yaml
esphome:
  name: energy-monitor
  libraries:
    - plerup/EspSoftwareSerial
    - PZEMPlus=https://github.com/lucashudson-eng/PZEMPlus.git#v0.7.3
  platformio_options:
    build_flags:
      - -DPZEM_6L24

external_components:
  - source:
      type: local
      path: components
    components: [pzem6l24_plus]

esp32:
  board: esp32-c3-devkitm-1
  framework:
    type: arduino

uart:
  id: uart_bus
  tx_pin: 4
  rx_pin: 5
  baud_rate: 9600

substitutions:
  pzem1: "Ground floor"
  pzem2: "First floor"

sensor:
  - platform: pzem6l24_plus
    id: pzem1
    address: 1
    rx_pin: 5
    tx_pin: 4
    de_re_pin: -1
    update_interval: 5s

    voltage_a:
      name: "Voltage Phase A"
    voltage_b:
      name: "Voltage Phase B"
    voltage_c:
      name: "Voltage Phase C"

    current_a:
      name: "${pzem1} Current A"
    current_b:
      name: "${pzem1} Current B"
    current_c:
      name: "${pzem1} Current C"      

    total_active_power:
      name: "${pzem1} Total Power"

    total_active_energy:
      name: "${pzem1} Total Energy"

  - platform: pzem6l24_plus
    id: pzem2
    address: 2
    rx_pin: 5
    tx_pin: 4
    de_re_pin: -1
    update_interval: 20s

    current_a:
      name: "${pzem2} Current A"
    current_b:
      name: "${pzem2} Current B"
    current_c:
      name: "${pzem2} Current C"

    total_active_power:
      name: "${pzem2} Total Power"

    total_active_energy:
      name: "${pzem2} Total Energy"
```

## Hardware Address Mode (DIP switches)

Enable DIP-switch Modbus addressing:

```yaml
esphome:
  on_boot:
    priority: -10
    then:
      - lambda: |-
          id(pzem1).use_hardware_address();
```

## Reset Energy

```yaml
script:
  - id: pzem1_reset_energy
    then:
      - lambda: |-
          id(pzem1).reset_energy_all();
```

Call this from Home Assistant.


