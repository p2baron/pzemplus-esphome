import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID

pzemplus_ns = cg.esphome_ns.namespace("pzemplus")
PZEM6L24Device = pzemplus_ns.class_("PZEM6L24Device", cg.PollingComponent)

CONF_ADDRESS = "address"
CONF_RX_PIN = "rx_pin"
CONF_TX_PIN = "tx_pin"
CONF_DE_RE_PIN = "de_re_pin"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(PZEM6L24Device),

        cv.Required(CONF_ADDRESS): cv.int_range(min=1, max=247),
        cv.Required(CONF_RX_PIN): cv.int_,
        cv.Required(CONF_TX_PIN): cv.int_,
        cv.Optional(CONF_DE_RE_PIN, default=-1): cv.int_,

        cv.Optional("voltage_a"): sensor.sensor_schema(
            unit_of_measurement="V",
            accuracy_decimals=1,
            device_class="voltage",
            state_class="measurement",
        ),
        cv.Optional("voltage_b"): sensor.sensor_schema(
            unit_of_measurement="V",
            accuracy_decimals=1,
            device_class="voltage",
            state_class="measurement",
        ),
        cv.Optional("voltage_c"): sensor.sensor_schema(
            unit_of_measurement="V",
            accuracy_decimals=1,
            device_class="voltage",
            state_class="measurement",
        ),

        cv.Optional("current_a"): sensor.sensor_schema(
            unit_of_measurement="A",
            accuracy_decimals=3,
            device_class="current",
            state_class="measurement",
        ),
        cv.Optional("current_b"): sensor.sensor_schema(
            unit_of_measurement="A",
            accuracy_decimals=3,
            device_class="current",
            state_class="measurement",
        ),
        cv.Optional("current_c"): sensor.sensor_schema(
            unit_of_measurement="A",
            accuracy_decimals=3,
            device_class="current",
            state_class="measurement",
        ),

        cv.Optional("total_active_power"): sensor.sensor_schema(
            unit_of_measurement="W",
            accuracy_decimals=1,
            device_class="power",
            state_class="measurement",
        ),
        cv.Optional("total_active_energy"): sensor.sensor_schema(
            unit_of_measurement="kWh",
            accuracy_decimals=3,
            device_class="energy",
            state_class="total_increasing",
        ),
    }
).extend(cv.polling_component_schema("5s"))


async def to_code(config):
    var = cg.new_Pvariable(
        config[CONF_ID],
        config[CONF_ADDRESS],
        config[CONF_RX_PIN],
        config[CONF_TX_PIN],
        config[CONF_DE_RE_PIN],
    )
    await cg.register_component(var, config)

    # Bind sensors if present
    for key in [
        "voltage_a",
        "voltage_b",
        "voltage_c",
        "current_a",
        "current_b",
        "current_c",
        "total_active_power",
        "total_active_energy",
    ]:
        if key in config:
            s = await sensor.new_sensor(config[key])
            cg.add(getattr(var, f"set_{key}_sensor")(s))

