import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_ID,
    CONF_ADDRESS,
    CONF_UPDATE_INTERVAL,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)

# Namespace + class
pzemplus_ns = cg.esphome_ns.namespace("pzemplus")
PZEM6L24Device = pzemplus_ns.class_("PZEM6L24Device", cg.PollingComponent)

CONF_RX_PIN = "rx_pin"
CONF_TX_PIN = "tx_pin"
CONF_DE_RE_PIN = "de_re_pin"

# Per-phase keys
CONF_VOLTAGE_A = "voltage_a"
CONF_VOLTAGE_B = "voltage_b"
CONF_VOLTAGE_C = "voltage_c"

CONF_CURRENT_A = "current_a"
CONF_CURRENT_B = "current_b"
CONF_CURRENT_C = "current_c"

CONF_FREQUENCY_A = "frequency_a"
CONF_FREQUENCY_B = "frequency_b"
CONF_FREQUENCY_C = "frequency_c"

CONF_ACTIVE_POWER_A = "active_power_a"
CONF_ACTIVE_POWER_B = "active_power_b"
CONF_ACTIVE_POWER_C = "active_power_c"

CONF_REACTIVE_POWER_A = "reactive_power_a"
CONF_REACTIVE_POWER_B = "reactive_power_b"
CONF_REACTIVE_POWER_C = "reactive_power_c"

CONF_APPARENT_POWER_A = "apparent_power_a"
CONF_APPARENT_POWER_B = "apparent_power_b"
CONF_APPARENT_POWER_C = "apparent_power_c"

CONF_POWER_FACTOR_A = "power_factor_a"
CONF_POWER_FACTOR_B = "power_factor_b"
CONF_POWER_FACTOR_C = "power_factor_c"

CONF_ACTIVE_ENERGY_A = "active_energy_a"
CONF_ACTIVE_ENERGY_B = "active_energy_b"
CONF_ACTIVE_ENERGY_C = "active_energy_c"

CONF_REACTIVE_ENERGY_A = "reactive_energy_a"
CONF_REACTIVE_ENERGY_B = "reactive_energy_b"
CONF_REACTIVE_ENERGY_C = "reactive_energy_c"

CONF_APPARENT_ENERGY_A = "apparent_energy_a"
CONF_APPARENT_ENERGY_B = "apparent_energy_b"
CONF_APPARENT_ENERGY_C = "apparent_energy_c"

CONF_VOLTAGE_PHASE_ANGLE_A = "voltage_phase_angle_a"
CONF_VOLTAGE_PHASE_ANGLE_B = "voltage_phase_angle_b"
CONF_VOLTAGE_PHASE_ANGLE_C = "voltage_phase_angle_c"

CONF_CURRENT_PHASE_ANGLE_A = "current_phase_angle_a"
CONF_CURRENT_PHASE_ANGLE_B = "current_phase_angle_b"
CONF_CURRENT_PHASE_ANGLE_C = "current_phase_angle_c"

# Totals (combined)
CONF_TOTAL_ACTIVE_POWER = "total_active_power"
CONF_TOTAL_REACTIVE_POWER = "total_reactive_power"
CONF_TOTAL_APPARENT_POWER = "total_apparent_power"
CONF_TOTAL_POWER_FACTOR = "total_power_factor"

CONF_TOTAL_ACTIVE_ENERGY = "total_active_energy"
CONF_TOTAL_REACTIVE_ENERGY = "total_reactive_energy"
CONF_TOTAL_APPARENT_ENERGY = "total_apparent_energy"

AUTO_LOAD = ["sensor"]

def _schema_voltage(icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="V",
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=icon,
    )

def _schema_current(icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="A",
        accuracy_decimals=3,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=icon,
    )

def _schema_frequency(icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="Hz",
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_FREQUENCY,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=icon,
    )

def _schema_power_kw(device_class=DEVICE_CLASS_POWER, icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="kW",
        accuracy_decimals=3,
        device_class=device_class,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=icon,
    )

def _schema_power_kvar(icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="kVar",
        accuracy_decimals=3,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=icon,
    )

def _schema_power_kva(icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="kVA",
        accuracy_decimals=3,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=icon,
    )

def _schema_pf(icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="PF",
        accuracy_decimals=3,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=icon,
    )

def _schema_energy_kwh(device_class=DEVICE_CLASS_ENERGY, icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="kWh",
        accuracy_decimals=3,
        device_class=device_class,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        icon=icon,
    )

def _schema_energy_kvarh(icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="kVarh",
        accuracy_decimals=3,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        icon=icon,
    )

def _schema_energy_kvah(icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="kVAh",
        accuracy_decimals=3,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        icon=icon,
    )

def _schema_angle(icon=None):
    return sensor.sensor_schema(
        unit_of_measurement="°",
        accuracy_decimals=1,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=icon,
    )

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PZEM6L24Device),
        cv.Required(CONF_ADDRESS): cv.int_range(min=1, max=247),

        # Pins for UART + RS-485 enable
        cv.Required(CONF_RX_PIN): cv.int_,
        cv.Required(CONF_TX_PIN): cv.int_,
        cv.Optional(CONF_DE_RE_PIN, default=-1): cv.int_,

        # Per-phase voltage/current
        cv.Optional(CONF_VOLTAGE_A): _schema_voltage("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_VOLTAGE_B): _schema_voltage("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_VOLTAGE_C): _schema_voltage("mdi:alpha-c-circle-outline"),

        cv.Optional(CONF_CURRENT_A): _schema_current("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_CURRENT_B): _schema_current("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_CURRENT_C): _schema_current("mdi:alpha-c-circle-outline"),

        # Per-phase frequency
        cv.Optional(CONF_FREQUENCY_A): _schema_frequency("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_FREQUENCY_B): _schema_frequency("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_FREQUENCY_C): _schema_frequency("mdi:alpha-c-circle-outline"),

        # Per-phase power
        cv.Optional(CONF_ACTIVE_POWER_A): _schema_power_kw(icon="mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_ACTIVE_POWER_B): _schema_power_kw(icon="mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_ACTIVE_POWER_C): _schema_power_kw(icon="mdi:alpha-c-circle-outline"),

        cv.Optional(CONF_REACTIVE_POWER_A): _schema_power_kvar("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_REACTIVE_POWER_B): _schema_power_kvar("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_REACTIVE_POWER_C): _schema_power_kvar("mdi:alpha-c-circle-outline"),

        cv.Optional(CONF_APPARENT_POWER_A): _schema_power_kva("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_APPARENT_POWER_B): _schema_power_kva("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_APPARENT_POWER_C): _schema_power_kva("mdi:alpha-c-circle-outline"),

        cv.Optional(CONF_POWER_FACTOR_A): _schema_pf("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_POWER_FACTOR_B): _schema_pf("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_POWER_FACTOR_C): _schema_pf("mdi:alpha-c-circle-outline"),

        # Per-phase energy
        cv.Optional(CONF_ACTIVE_ENERGY_A): _schema_energy_kwh(icon="mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_ACTIVE_ENERGY_B): _schema_energy_kwh(icon="mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_ACTIVE_ENERGY_C): _schema_energy_kwh(icon="mdi:alpha-c-circle-outline"),

        cv.Optional(CONF_REACTIVE_ENERGY_A): _schema_energy_kvarh("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_REACTIVE_ENERGY_B): _schema_energy_kvarh("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_REACTIVE_ENERGY_C): _schema_energy_kvarh("mdi:alpha-c-circle-outline"),

        cv.Optional(CONF_APPARENT_ENERGY_A): _schema_energy_kvah("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_APPARENT_ENERGY_B): _schema_energy_kvah("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_APPARENT_ENERGY_C): _schema_energy_kvah("mdi:alpha-c-circle-outline"),

        # Phase angles
        cv.Optional(CONF_VOLTAGE_PHASE_ANGLE_A): _schema_angle("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_VOLTAGE_PHASE_ANGLE_B): _schema_angle("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_VOLTAGE_PHASE_ANGLE_C): _schema_angle("mdi:alpha-c-circle-outline"),

        cv.Optional(CONF_CURRENT_PHASE_ANGLE_A): _schema_angle("mdi:alpha-a-circle-outline"),
        cv.Optional(CONF_CURRENT_PHASE_ANGLE_B): _schema_angle("mdi:alpha-b-circle-outline"),
        cv.Optional(CONF_CURRENT_PHASE_ANGLE_C): _schema_angle("mdi:alpha-c-circle-outline"),

        # Totals (combined)
        cv.Optional(CONF_TOTAL_ACTIVE_POWER): _schema_power_kw(icon="mdi:flash"),
        cv.Optional(CONF_TOTAL_REACTIVE_POWER): _schema_power_kvar(icon="mdi:flash"),
        cv.Optional(CONF_TOTAL_APPARENT_POWER): _schema_power_kva(icon="mdi:flash"),
        cv.Optional(CONF_TOTAL_POWER_FACTOR): _schema_pf(icon="mdi:flash"),

        cv.Optional(CONF_TOTAL_ACTIVE_ENERGY): _schema_energy_kwh(icon="mdi:counter"),
        cv.Optional(CONF_TOTAL_REACTIVE_ENERGY): _schema_energy_kvarh(icon="mdi:counter"),
        cv.Optional(CONF_TOTAL_APPARENT_ENERGY): _schema_energy_kvah(icon="mdi:counter"),
    }
).extend(cv.polling_component_schema("5s"))


async def _set_s(var, config, key, make_setter):
    if key in config:
        sens = await sensor.new_sensor(config[key])
        cg.add(make_setter(sens))


async def _set_phase(var, config, key, phase, setter_name):
    if key in config:
        sens = await sensor.new_sensor(config[key])
        cg.add(getattr(var, setter_name)(phase, sens))


async def to_code(config):
    var = cg.new_Pvariable(
        config[CONF_ID],
        config[CONF_ADDRESS],
        config[CONF_RX_PIN],
        config[CONF_TX_PIN],
        config[CONF_DE_RE_PIN],
        config[CONF_UPDATE_INTERVAL].total_milliseconds,
    )
    await cg.register_component(var, config)

    # Per-phase mapping: 0=A, 1=B, 2=C
    await _set_phase(var, config, CONF_VOLTAGE_A, 0, "set_voltage_sensor")
    await _set_phase(var, config, CONF_VOLTAGE_B, 1, "set_voltage_sensor")
    await _set_phase(var, config, CONF_VOLTAGE_C, 2, "set_voltage_sensor")

    await _set_phase(var, config, CONF_CURRENT_A, 0, "set_current_sensor")
    await _set_phase(var, config, CONF_CURRENT_B, 1, "set_current_sensor")
    await _set_phase(var, config, CONF_CURRENT_C, 2, "set_current_sensor")

    await _set_phase(var, config, CONF_FREQUENCY_A, 0, "set_frequency_sensor")
    await _set_phase(var, config, CONF_FREQUENCY_B, 1, "set_frequency_sensor")
    await _set_phase(var, config, CONF_FREQUENCY_C, 2, "set_frequency_sensor")

    await _set_phase(var, config, CONF_ACTIVE_POWER_A, 0, "set_active_power_sensor")
    await _set_phase(var, config, CONF_ACTIVE_POWER_B, 1, "set_active_power_sensor")
    await _set_phase(var, config, CONF_ACTIVE_POWER_C, 2, "set_active_power_sensor")

    await _set_phase(var, config, CONF_REACTIVE_POWER_A, 0, "set_reactive_power_sensor")
    await _set_phase(var, config, CONF_REACTIVE_POWER_B, 1, "set_reactive_power_sensor")
    await _set_phase(var, config, CONF_REACTIVE_POWER_C, 2, "set_reactive_power_sensor")

    await _set_phase(var, config, CONF_APPARENT_POWER_A, 0, "set_apparent_power_sensor")
    await _set_phase(var, config, CONF_APPARENT_POWER_B, 1, "set_apparent_power_sensor")
    await _set_phase(var, config, CONF_APPARENT_POWER_C, 2, "set_apparent_power_sensor")

    await _set_phase(var, config, CONF_POWER_FACTOR_A, 0, "set_power_factor_sensor")
    await _set_phase(var, config, CONF_POWER_FACTOR_B, 1, "set_power_factor_sensor")
    await _set_phase(var, config, CONF_POWER_FACTOR_C, 2, "set_power_factor_sensor")

    await _set_phase(var, config, CONF_ACTIVE_ENERGY_A, 0, "set_active_energy_sensor")
    await _set_phase(var, config, CONF_ACTIVE_ENERGY_B, 1, "set_active_energy_sensor")
    await _set_phase(var, config, CONF_ACTIVE_ENERGY_C, 2, "set_active_energy_sensor")

    await _set_phase(var, config, CONF_REACTIVE_ENERGY_A, 0, "set_reactive_energy_sensor")
    await _set_phase(var, config, CONF_REACTIVE_ENERGY_B, 1, "set_reactive_energy_sensor")
    await _set_phase(var, config, CONF_REACTIVE_ENERGY_C, 2, "set_reactive_energy_sensor")

    await _set_phase(var, config, CONF_APPARENT_ENERGY_A, 0, "set_apparent_energy_sensor")
    await _set_phase(var, config, CONF_APPARENT_ENERGY_B, 1, "set_apparent_energy_sensor")
    await _set_phase(var, config, CONF_APPARENT_ENERGY_C, 2, "set_apparent_energy_sensor")

    await _set_phase(var, config, CONF_VOLTAGE_PHASE_ANGLE_A, 0, "set_voltage_phase_angle_sensor")
    await _set_phase(var, config, CONF_VOLTAGE_PHASE_ANGLE_B, 1, "set_voltage_phase_angle_sensor")
    await _set_phase(var, config, CONF_VOLTAGE_PHASE_ANGLE_C, 2, "set_voltage_phase_angle_sensor")

    await _set_phase(var, config, CONF_CURRENT_PHASE_ANGLE_A, 0, "set_current_phase_angle_sensor")
    await _set_phase(var, config, CONF_CURRENT_PHASE_ANGLE_B, 1, "set_current_phase_angle_sensor")
    await _set_phase(var, config, CONF_CURRENT_PHASE_ANGLE_C, 2, "set_current_phase_angle_sensor")

    # Totals
    await _set_s(var, config, CONF_TOTAL_ACTIVE_POWER, var.set_total_active_power_sensor)
    await _set_s(var, config, CONF_TOTAL_REACTIVE_POWER, var.set_total_reactive_power_sensor)
    await _set_s(var, config, CONF_TOTAL_APPARENT_POWER, var.set_total_apparent_power_sensor)
    await _set_s(var, config, CONF_TOTAL_POWER_FACTOR, var.set_total_power_factor_sensor)

    await _set_s(var, config, CONF_TOTAL_ACTIVE_ENERGY, var.set_total_active_energy_sensor)
    await _set_s(var, config, CONF_TOTAL_REACTIVE_ENERGY, var.set_total_reactive_energy_sensor)
    await _set_s(var, config, CONF_TOTAL_APPARENT_ENERGY, var.set_total_apparent_energy_sensor)
