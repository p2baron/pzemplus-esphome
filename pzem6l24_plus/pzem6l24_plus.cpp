#include "pzem6l24_plus.h"

#include "esphome/core/log.h"

static const char *const TAG = "pzem6l24_plus";

namespace esphome {
namespace pzemplus {

HardwareSerial PZEM6L24Device::serial_(1);
bool PZEM6L24Device::serial_initialized_ = false;

PZEM6L24Device::PZEM6L24Device(uint8_t address, int rx_pin, int tx_pin, int8_t de_re_pin)
    : PollingComponent(),
      address_(address),
      rx_pin_(rx_pin),
      tx_pin_(tx_pin),
      de_re_pin_(de_re_pin),
      pzem_(serial_, address) {}

void PZEM6L24Device::setup() {
  ESP_LOGI(TAG, "Setup PZEM6L24 addr=%u rx=%d tx=%d de_re=%d",address_, rx_pin_, tx_pin_, de_re_pin_);
  if (!serial_initialized_) {
    serial_.begin(9600, SERIAL_8N1, rx_pin_, tx_pin_);
    serial_initialized_ = true;
  }

  if (de_re_pin_ > -1) {
    pinMode(de_re_pin_, OUTPUT);
    digitalWrite(de_re_pin_, LOW);
    pzem_.setEnable(de_re_pin_);
  }

  pzem_.begin();
  pzem_.setBaudrateAndConnectionType(9600, PZEM_CONNECTION_3PHASE_4WIRE);
  pzem_.setFrequency(50);
}

void PZEM6L24Device::update() {
  float vA = NAN, vB = NAN, vC = NAN;
  float cA = NAN, cB = NAN, cC = NAN;

  ESP_LOGV(TAG, "Polling PZEM address %u", address_);

  pzem_.readVoltage(vA, vB, vC);
  pzem_.readCurrent(cA, cB, cC);

  float totalP = pzem_.readActivePower();
  float totalE = pzem_.readActiveEnergy();

  ESP_LOGV(TAG, "Read: V=[%.1f, %.1f, %.1f]  I=[%.3f, %.3f, %.3f]  P=%.1f  E=%.3f",vA, vB, vC, cA, cB, cC, totalP, totalE);

  auto publish_if_valid = [](sensor::Sensor *s, float value) {
   if (s == nullptr) return;
   if (isnan(value)) return;
   s->publish_state(value);
  };

  publish_if_valid(voltage_a_, vA);
  publish_if_valid(voltage_b_, vB);
  publish_if_valid(voltage_c_, vC);

  publish_if_valid(current_a_, cA);
  publish_if_valid(current_b_, cB);
  publish_if_valid(current_c_, cC);
  
  publish_if_valid(total_power_, totalP);
  publish_if_valid(total_energy_, totalE);

}

void PZEM6L24Device::use_hardware_address() {
  ESP_LOGI(TAG, "Setting PZEM addr=%u to use HARDWARE (DIP) address mode", address_);
  // For PZEM-6L24, setAddress(0x00) = use DIP switch address
  pzem_.setAddress(0x00);
}

void PZEM6L24Device::reset_energy_all() {
  ESP_LOGI(TAG, "Resetting energy (ALL phases) on PZEM addr=%u", address_);
  // Reset all phase energy counters
  pzem_.resetEnergy(PZEM_RESET_ENERGY_ALL);
}


}  // namespace pzemplus
}  // namespace esphome

