#pragma once

#include "esphome.h"
#include "esphome/components/sensor/sensor.h"  // <-- needed for sensor::Sensor
#include <HardwareSerial.h>
#include <PZEMPlus.h>

namespace esphome {
namespace pzemplus {

class PZEM6L24Device : public PollingComponent {
 public:
  PZEM6L24Device(uint8_t address, int rx_pin, int tx_pin, int8_t de_re_pin);

  void setup() override;
  void update() override;

  /// Tell the device to use its hardware (DIP switch) address
  void use_hardware_address();

  /// Reset all phase energy counters (PZEM_RESET_ENERGY_ALL)
  void reset_energy_all();

  // Sensor setters (called from Python)
  void set_voltage_a_sensor(sensor::Sensor *s) { voltage_a_ = s; }
  void set_voltage_b_sensor(sensor::Sensor *s) { voltage_b_ = s; }
  void set_voltage_c_sensor(sensor::Sensor *s) { voltage_c_ = s; }

  void set_current_a_sensor(sensor::Sensor *s) { current_a_ = s; }
  void set_current_b_sensor(sensor::Sensor *s) { current_b_ = s; }
  void set_current_c_sensor(sensor::Sensor *s) { current_c_ = s; }

  void set_total_active_power_sensor(sensor::Sensor *s) { total_power_ = s; }
  void set_total_active_energy_sensor(sensor::Sensor *s) { total_energy_ = s; }

 protected:
  uint8_t address_;
  int rx_pin_;
  int tx_pin_;
  int8_t de_re_pin_;

  // Shared UART for all PZEM-6L24 devices
  static HardwareSerial serial_;
  static bool serial_initialized_;

  PZEMPlus pzem_;

  sensor::Sensor *voltage_a_{nullptr};
  sensor::Sensor *voltage_b_{nullptr};
  sensor::Sensor *voltage_c_{nullptr};

  sensor::Sensor *current_a_{nullptr};
  sensor::Sensor *current_b_{nullptr};
  sensor::Sensor *current_c_{nullptr};

  sensor::Sensor *total_power_{nullptr};
  sensor::Sensor *total_energy_{nullptr};
};

}  // namespace pzemplus
}  // namespace esphome

