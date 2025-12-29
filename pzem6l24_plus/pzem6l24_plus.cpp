#include "pzem6l24_plus.h"

namespace esphome {
namespace pzemplus {

HardwareSerial PZEM6L24Device::pzem_serial_(1);
bool PZEM6L24Device::serial_initialized_ = false;

PZEM6L24Device::PZEM6L24Device(uint8_t address, int rx_pin, int tx_pin, int8_t de_re_pin,
                               uint32_t update_interval_ms)
    : PollingComponent(update_interval_ms),
      address_(address),
      rx_pin_(rx_pin),
      tx_pin_(tx_pin),
      de_re_pin_(de_re_pin),
      pzem_(pzem_serial_, address) {}

void PZEM6L24Device::setup() {
  // Init shared UART once
  if (!serial_initialized_) {
    pzem_serial_.begin(9600, SERIAL_8N1, rx_pin_, tx_pin_);
    serial_initialized_ = true;
  }

  // Optional RS-485 enable pin (DE+RE)
  if (de_re_pin_ >= 0) {
    pinMode(de_re_pin_, OUTPUT);
    digitalWrite(de_re_pin_, LOW);  // typical: LOW=receive
    pzem_.setEnable(de_re_pin_);
  }

  pzem_.begin();

  // Grid config (change frequency to 60 if needed)
  pzem_.setBaudrateAndConnectionType(9600, PZEM_CONNECTION_3PHASE_4WIRE);
  pzem_.setFrequency(50);
}

bool PZEM6L24Device::use_hardware_address() {
  bool ok = pzem_.setAddress(0x00);
  ESP_LOGI("pzem6l24_plus", "setAddress(0x00) hardware addressing: %s", ok ? "OK" : "FAIL");
  return ok;
}

bool PZEM6L24Device::set_software_address(uint8_t address) {
  bool ok = pzem_.setAddress(address);
  ESP_LOGI("pzem6l24_plus", "setAddress(0x%02X) software addressing: %s", address, ok ? "OK" : "FAIL");
  return ok;
}

bool PZEM6L24Device::reset_energy_all() {
  bool ok = pzem_.resetEnergy(PZEM_RESET_ENERGY_ALL);
  ESP_LOGI("pzem6l24_plus", "resetEnergy(PZEM_RESET_ENERGY_ALL): %s", ok ? "OK" : "FAIL");
  return ok;
}

static inline void publish_if(sensor::Sensor *s, float v) {
  if (s != nullptr && !isnan(v)) s->publish_state(v);
}

void PZEM6L24Device::update() {
  // Per-phase mapping: 0=A, 1=B, 2=C
  for (uint8_t ph = 0; ph < 3; ph++) {
    // V, A, Hz
    publish_if(voltage_[ph], pzem_.readVoltage(ph));
    publish_if(current_[ph], pzem_.readCurrent(ph));
    publish_if(frequency_[ph], pzem_.readFrequency(ph));

    // Power: W/VAR/VA -> kW/kVar/kVA
    publish_if(active_power_[ph],   pzem_.readActivePower(ph)   / 1000.0f);
    publish_if(reactive_power_[ph], pzem_.readReactivePower(ph) / 1000.0f);
    publish_if(apparent_power_[ph], pzem_.readApparentPower(ph) / 1000.0f);

    // PF
    publish_if(power_factor_[ph], pzem_.readPowerFactor(ph));

    // Energy: Wh/VARh/VAh -> kWh/kVarh/kVAh
    publish_if(active_energy_[ph],   pzem_.readActiveEnergy(ph)   / 1000.0f);
    publish_if(reactive_energy_[ph], pzem_.readReactiveEnergy(ph) / 1000.0f);
    publish_if(apparent_energy_[ph], pzem_.readApparentEnergy(ph) / 1000.0f);

    // Angles: degrees
    publish_if(v_angle_[ph], pzem_.readVoltagePhaseAngle(ph));
    publish_if(i_angle_[ph], pzem_.readCurrentPhaseAngle(ph));
  }

  // Totals (combined all phases): W/VAR/VA -> kW/kVar/kVA; Wh -> kWh
  publish_if(total_active_power_,   pzem_.readActivePower()   / 1000.0f);
  publish_if(total_reactive_power_, pzem_.readReactivePower() / 1000.0f);
  publish_if(total_apparent_power_, pzem_.readApparentPower() / 1000.0f);
  publish_if(total_power_factor_,   pzem_.readPowerFactor());

  publish_if(total_active_energy_,   pzem_.readActiveEnergy()   / 1000.0f);
  publish_if(total_reactive_energy_, pzem_.readReactiveEnergy() / 1000.0f);
  publish_if(total_apparent_energy_, pzem_.readApparentEnergy() / 1000.0f);
}

}  // namespace pzemplus
}  // namespace esphome
