#pragma once

#ifndef PZEM_6L24
#define PZEM_6L24
#endif

#include "esphome.h"
#include <HardwareSerial.h>
#include <PZEMPlus.h>

namespace esphome {
namespace pzemplus {

class PZEM6L24Device : public PollingComponent {
 public:
  PZEM6L24Device(uint8_t address, int rx_pin, int tx_pin, int8_t de_re_pin,
                 uint32_t update_interval_ms);

  void setup() override;
  void update() override;

  // ===== Methods you want to call from YAML lambdas =====
  // Use hardware addressing (address = 0x00)
  bool use_hardware_address();

  // Reset all energy counters (A, B, C, combined)
  bool reset_energy_all();

  // Optional: set explicit software address (1..247)
  bool set_software_address(uint8_t address);

  // Per-phase setters (phase: 0=A,1=B,2=C)
  void set_voltage_sensor(uint8_t phase, sensor::Sensor *s) { voltage_[phase] = s; }
  void set_current_sensor(uint8_t phase, sensor::Sensor *s) { current_[phase] = s; }

  void set_frequency_sensor(uint8_t phase, sensor::Sensor *s) { frequency_[phase] = s; }
  void set_active_power_sensor(uint8_t phase, sensor::Sensor *s) { active_power_[phase] = s; }
  void set_reactive_power_sensor(uint8_t phase, sensor::Sensor *s) { reactive_power_[phase] = s; }
  void set_apparent_power_sensor(uint8_t phase, sensor::Sensor *s) { apparent_power_[phase] = s; }
  void set_power_factor_sensor(uint8_t phase, sensor::Sensor *s) { power_factor_[phase] = s; }

  void set_active_energy_sensor(uint8_t phase, sensor::Sensor *s) { active_energy_[phase] = s; }
  void set_reactive_energy_sensor(uint8_t phase, sensor::Sensor *s) { reactive_energy_[phase] = s; }
  void set_apparent_energy_sensor(uint8_t phase, sensor::Sensor *s) { apparent_energy_[phase] = s; }

  void set_voltage_phase_angle_sensor(uint8_t phase, sensor::Sensor *s) { v_angle_[phase] = s; }
  void set_current_phase_angle_sensor(uint8_t phase, sensor::Sensor *s) { i_angle_[phase] = s; }

  // Totals (combined 3-phase)
  void set_total_active_power_sensor(sensor::Sensor *s) { total_active_power_ = s; }
  void set_total_reactive_power_sensor(sensor::Sensor *s) { total_reactive_power_ = s; }
  void set_total_apparent_power_sensor(sensor::Sensor *s) { total_apparent_power_ = s; }
  void set_total_power_factor_sensor(sensor::Sensor *s) { total_power_factor_ = s; }

  void set_total_active_energy_sensor(sensor::Sensor *s) { total_active_energy_ = s; }
  void set_total_reactive_energy_sensor(sensor::Sensor *s) { total_reactive_energy_ = s; }
  void set_total_apparent_energy_sensor(sensor::Sensor *s) { total_apparent_energy_ = s; }

 protected:
  uint8_t address_;
  int rx_pin_;
  int tx_pin_;
  int8_t de_re_pin_;

  sensor::Sensor *voltage_[3]{nullptr, nullptr, nullptr};
  sensor::Sensor *current_[3]{nullptr, nullptr, nullptr};

  sensor::Sensor *frequency_[3]{nullptr, nullptr, nullptr};
  sensor::Sensor *active_power_[3]{nullptr, nullptr, nullptr};
  sensor::Sensor *reactive_power_[3]{nullptr, nullptr, nullptr};
  sensor::Sensor *apparent_power_[3]{nullptr, nullptr, nullptr};
  sensor::Sensor *power_factor_[3]{nullptr, nullptr, nullptr};

  sensor::Sensor *active_energy_[3]{nullptr, nullptr, nullptr};
  sensor::Sensor *reactive_energy_[3]{nullptr, nullptr, nullptr};
  sensor::Sensor *apparent_energy_[3]{nullptr, nullptr, nullptr};

  sensor::Sensor *v_angle_[3]{nullptr, nullptr, nullptr};
  sensor::Sensor *i_angle_[3]{nullptr, nullptr, nullptr};

  sensor::Sensor *total_active_power_{nullptr};
  sensor::Sensor *total_reactive_power_{nullptr};
  sensor::Sensor *total_apparent_power_{nullptr};
  sensor::Sensor *total_power_factor_{nullptr};

  sensor::Sensor *total_active_energy_{nullptr};
  sensor::Sensor *total_reactive_energy_{nullptr};
  sensor::Sensor *total_apparent_energy_{nullptr};

  // Shared UART for all instances on same RS-485 bus
  static HardwareSerial pzem_serial_;
  static bool serial_initialized_;

  PZEMPlus pzem_;
};

}  // namespace pzemplus
}  // namespace esphome
