
# PZEM-6L24 External Component for ESPHome

Support for single- and three-phase PZEM-6L24 energy meters using the **lucashudson-eng/PZEMPlus** Arduino library.


## Tested with

- ESPHome 2025.11+
- ESP32-C3 
- PZEM-6L24 energy meter(s)
- MAX3485 / MAX485 RS-485 module
- lucashudson-eng/PZEMPlus library v0.71


## Directory Structure

```
components/
  pzem6l24_plus/
    __init__.py
    sensor.py
    pzem6l24_plus.h
    pzem6l24_plus.cpp
```

## ESPHome YAML Example

```yaml
esphome:
  name: energy-monitor
  libraries:
    - PZEMPlus=https://github.com/lucashudson-eng/PZEMPlus.git

external_components:
  - source:
      type: local
      path: components

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
      name: "Voltage Pahse B"
    voltage_c:
      name: "Voltage Pahce C"

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

## Known Limitations

- ESPHome `button:` component may cause linking issues on ESP32-C3.  
  Use HA-side buttons or scripts instead.
- Not all function's from Lucas his library are linked.
- Calibration routine is not implemeted in PZEM library. 

