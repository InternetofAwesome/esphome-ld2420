import esphome.codegen as cg
from esphome.components import sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_MOVING_DISTANCE,
    DEVICE_CLASS_DISTANCE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CENTIMETER,
)

from .. import CONF_LD2420_ID, LD2420Component, ld2420_ns

LD2420Sensor = ld2420_ns.class_("LD2420Sensor", sensor.Sensor, cg.Component)

TOTAL_GATES = 16

CONFIG_SCHEMA = cv.All(
    cv.COMPONENT_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(LD2420Sensor),
            cv.GenerateID(CONF_LD2420_ID): cv.use_id(LD2420Component),
            cv.Optional(CONF_MOVING_DISTANCE): sensor.sensor_schema(
                device_class=DEVICE_CLASS_DISTANCE,
                unit_of_measurement=UNIT_CENTIMETER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            **{
                cv.Optional(f"gate_energy_{x}"): sensor.sensor_schema(
                    state_class=STATE_CLASS_MEASUREMENT,
                )
                for x in range(TOTAL_GATES)
            },
        }
    ),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    if CONF_MOVING_DISTANCE in config:
        sens = await sensor.new_sensor(config[CONF_MOVING_DISTANCE])
        cg.add(var.set_distance_sensor(sens))
    for x in range(TOTAL_GATES):
        if (gate_conf := config.get(f"gate_energy_{x}")) is not None:
            sens = await sensor.new_sensor(gate_conf)
            cg.add(var.set_gate_energy_sensor(x, sens))
    ld2420 = await cg.get_variable(config[CONF_LD2420_ID])
    cg.add(ld2420.register_listener(var))
