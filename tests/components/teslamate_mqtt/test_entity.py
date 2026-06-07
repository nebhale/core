"""Tests for TeslaMate MQTT entities."""

import asyncio
from collections.abc import Callable, Coroutine
import logging
from typing import Any
from unittest.mock import patch

import pytest

from homeassistant.components import mqtt
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import (
    ATTR_STATE_CLASS,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.components.teslamate_mqtt.const import CONF_TOPIC_ROOT, DOMAIN
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_GPS_ACCURACY,
    ATTR_ICON,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_UNIT_OF_MEASUREMENT,
    DEGREE,
    PERCENTAGE,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfLength,
    UnitOfPower,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er

from tests.common import MockConfigEntry, async_fire_mqtt_message
from tests.typing import MqttMockHAClient


@callback
def _async_on_subscribe_done(
    hass: HomeAssistant,
    topic: str,
    qos: int,
    on_subscribe_status: Callable[[], None],
) -> CALLBACK_TYPE:
    """Call the MQTT subscribe status callback immediately."""
    on_subscribe_status()
    return lambda: None


async def _async_setup_entry(
    hass: HomeAssistant,
    topic_root: str = "teslamate/cars/1",
    display_name: str = "Roadrunner",
) -> MockConfigEntry:
    """Set up a TeslaMate MQTT config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=display_name,
        data={CONF_TOPIC_ROOT: topic_root},
        unique_id=topic_root,
    )
    entry.add_to_hass(hass)

    subscribe_started = asyncio.Event()
    real_async_subscribe = mqtt.async_subscribe

    async def async_subscribe(
        hass: HomeAssistant,
        topic: str,
        msg_callback: Callable[[mqtt.ReceiveMessage], Coroutine[Any, Any, None] | None],
        qos: int = 0,
        encoding: str | None = "utf-8",
    ) -> CALLBACK_TYPE:
        """Subscribe to MQTT and mark the subscription as started."""
        unsub = await real_async_subscribe(hass, topic, msg_callback, qos, encoding)
        subscribe_started.set()
        return unsub

    with (
        patch(
            "homeassistant.components.teslamate_mqtt.mqtt.async_on_subscribe_done",
            side_effect=_async_on_subscribe_done,
        ),
        patch(
            "homeassistant.components.teslamate_mqtt.mqtt.async_subscribe",
            side_effect=async_subscribe,
        ),
    ):
        setup_task = hass.async_create_task(
            hass.config_entries.async_setup(entry.entry_id)
        )
        await subscribe_started.wait()
        async_fire_mqtt_message(
            hass, f"{topic_root}/display_name", display_name, retain=True
        )
        assert await setup_task
    await hass.async_block_till_done()

    return entry


async def test_entities(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test TeslaMate MQTT entities."""
    entry = await _async_setup_entry(hass)

    assert hass.states.get("binary_sensor.roadrunner_charge_port").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_doors").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_door_driver_front").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_door_driver_rear").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_door_passenger_front").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_door_passenger_rear").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_frunk").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_health").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_climate").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_preconditioning").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("binary_sensor.roadrunner_occupancy").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_lock").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_plug").state == STATE_UNKNOWN
    assert hass.states.get("binary_sensor.roadrunner_sentry_mode").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("device_tracker.roadrunner").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_battery").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_center_display").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_energy_added").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charge_limit").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charge_current_request").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_charge_current_request_max").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_charger_current").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charger_phases").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charger_power").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charger_voltage").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_charging_state").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_climate_keeper").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_display_name") is None
    assert hass.states.get("sensor.roadrunner_elevation").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_exterior_color").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_geofence").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_heading").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_temperature_inside").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_temperature_outside").state == (
        STATE_UNKNOWN
    )
    assert hass.states.get("sensor.roadrunner_odometer").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_power").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_range_estimated").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_range_ideal").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_range_rated").state == STATE_UNKNOWN
    assert hass.states.get(
        "sensor.roadrunner_charging_start_time"
    ).state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_shift_state").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_last_seen").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_speed").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_spoiler_type").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_version").state == STATE_UNKNOWN

    async_fire_mqtt_message(hass, "teslamate/cars/1/charge_port_door_open", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/doors_open", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/driver_front_door_open", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/driver_rear_door_open", "false")
    async_fire_mqtt_message(
        hass, "teslamate/cars/1/passenger_front_door_open", "true"
    )
    async_fire_mqtt_message(
        hass, "teslamate/cars/1/passenger_rear_door_open", "false"
    )
    async_fire_mqtt_message(hass, "teslamate/cars/1/frunk_open", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/healthy", "false")
    async_fire_mqtt_message(hass, "teslamate/cars/1/is_climate_on", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/is_preconditioning", "false")
    async_fire_mqtt_message(hass, "teslamate/cars/1/is_user_present", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/locked", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/plugged_in", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/sentry_mode", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/latitude", "37.123")
    async_fire_mqtt_message(hass, "teslamate/cars/1/longitude", "-122.456")
    async_fire_mqtt_message(hass, "teslamate/cars/1/battery_level", "74")
    async_fire_mqtt_message(hass, "teslamate/cars/1/center_display_state", "8")
    async_fire_mqtt_message(hass, "teslamate/cars/1/charge_energy_added", "12.3")
    async_fire_mqtt_message(hass, "teslamate/cars/1/charge_limit_soc", "80")
    async_fire_mqtt_message(hass, "teslamate/cars/1/charge_current_request", "24")
    async_fire_mqtt_message(hass, "teslamate/cars/1/charge_current_request_max", "48")
    async_fire_mqtt_message(hass, "teslamate/cars/1/charger_actual_current", "40")
    async_fire_mqtt_message(hass, "teslamate/cars/1/charger_phases", "3")
    async_fire_mqtt_message(hass, "teslamate/cars/1/charger_power", "11")
    async_fire_mqtt_message(hass, "teslamate/cars/1/charger_voltage", "240")
    async_fire_mqtt_message(hass, "teslamate/cars/1/charging_state", "NoPower")
    async_fire_mqtt_message(hass, "teslamate/cars/1/climate_keeper_mode", "dog")
    async_fire_mqtt_message(hass, "teslamate/cars/1/elevation", "123")
    async_fire_mqtt_message(hass, "teslamate/cars/1/exterior_color", "DeepBlue")
    async_fire_mqtt_message(hass, "teslamate/cars/1/geofence", "Home")
    async_fire_mqtt_message(hass, "teslamate/cars/1/heading", "270")
    async_fire_mqtt_message(hass, "teslamate/cars/1/inside_temp", "22.4")
    async_fire_mqtt_message(hass, "teslamate/cars/1/outside_temp", "18.7")
    async_fire_mqtt_message(hass, "teslamate/cars/1/odometer", "12345.6")
    async_fire_mqtt_message(hass, "teslamate/cars/1/power", "-7")
    async_fire_mqtt_message(hass, "teslamate/cars/1/est_battery_range_km", "321.5")
    async_fire_mqtt_message(hass, "teslamate/cars/1/ideal_battery_range_km", "330.1")
    async_fire_mqtt_message(hass, "teslamate/cars/1/rated_battery_range_km", "325.7")
    async_fire_mqtt_message(
        hass,
        "teslamate/cars/1/scheduled_charging_start_time",
        "2026-06-07T12:34:56+00:00",
    )
    async_fire_mqtt_message(hass, "teslamate/cars/1/shift_state", "D")
    async_fire_mqtt_message(hass, "teslamate/cars/1/since", "2026-06-07T12:00:00+00:00")
    async_fire_mqtt_message(hass, "teslamate/cars/1/speed", "88")
    async_fire_mqtt_message(hass, "teslamate/cars/1/spoiler_type", "CarbonFiber")
    async_fire_mqtt_message(hass, "teslamate/cars/1/version", "2026.14.1")
    async_fire_mqtt_message(hass, "teslamate/cars/1/model", "3")
    async_fire_mqtt_message(hass, "teslamate/cars/1/trim_badging", "Performance")
    await hass.async_block_till_done()

    charge_port_state = hass.states.get("binary_sensor.roadrunner_charge_port")
    assert charge_port_state.state == STATE_ON
    assert charge_port_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.DOOR
    assert charge_port_state.attributes[ATTR_ICON] == "mdi:ev-plug-tesla"

    assert hass.states.get("binary_sensor.roadrunner_doors").state == STATE_ON
    assert (
        hass.states.get("binary_sensor.roadrunner_doors").attributes[ATTR_ICON]
        == "mdi:car-door"
    )

    driver_front_door_state = hass.states.get(
        "binary_sensor.roadrunner_door_driver_front"
    )
    assert driver_front_door_state.state == STATE_ON
    assert (
        driver_front_door_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.DOOR
    )
    assert driver_front_door_state.attributes[ATTR_ICON] == "mdi:car-door"

    driver_rear_door_state = hass.states.get(
        "binary_sensor.roadrunner_door_driver_rear"
    )
    assert driver_rear_door_state.state == STATE_OFF
    assert (
        driver_rear_door_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.DOOR
    )
    assert driver_rear_door_state.attributes[ATTR_ICON] == "mdi:car-door"

    passenger_front_door_state = hass.states.get(
        "binary_sensor.roadrunner_door_passenger_front"
    )
    assert passenger_front_door_state.state == STATE_ON
    assert (
        passenger_front_door_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.DOOR
    )
    assert passenger_front_door_state.attributes[ATTR_ICON] == "mdi:car-door"

    passenger_rear_door_state = hass.states.get(
        "binary_sensor.roadrunner_door_passenger_rear"
    )
    assert passenger_rear_door_state.state == STATE_OFF
    assert (
        passenger_rear_door_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.DOOR
    )
    assert passenger_rear_door_state.attributes[ATTR_ICON] == "mdi:car-door"

    frunk_state = hass.states.get("binary_sensor.roadrunner_frunk")
    assert frunk_state.state == STATE_ON
    assert frunk_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.DOOR
    assert frunk_state.attributes[ATTR_ICON] == "mdi:car"

    health_state = hass.states.get("binary_sensor.roadrunner_health")
    assert health_state.state == STATE_ON
    assert health_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.PROBLEM
    assert health_state.attributes[ATTR_ICON] == "mdi:heart-pulse"

    climate_state = hass.states.get("binary_sensor.roadrunner_climate")
    assert climate_state.state == STATE_ON
    assert (
        climate_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.RUNNING
    )
    assert climate_state.attributes[ATTR_ICON] == "mdi:air-conditioner"

    preconditioning_state = hass.states.get("binary_sensor.roadrunner_preconditioning")
    assert preconditioning_state.state == STATE_OFF
    assert (
        preconditioning_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.RUNNING
    )
    assert preconditioning_state.attributes[ATTR_ICON] == "mdi:air-conditioner"

    occupied_state = hass.states.get("binary_sensor.roadrunner_occupancy")
    assert occupied_state.state == STATE_ON
    assert (
        occupied_state.attributes[ATTR_DEVICE_CLASS]
        == BinarySensorDeviceClass.OCCUPANCY
    )
    assert occupied_state.attributes[ATTR_ICON] == "mdi:account"

    locked_state = hass.states.get("binary_sensor.roadrunner_lock")
    assert locked_state.state == STATE_OFF
    assert locked_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.LOCK

    plug_state = hass.states.get("binary_sensor.roadrunner_plug")
    assert plug_state.state == STATE_ON
    assert plug_state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.PLUG

    sentry_mode = hass.states.get("binary_sensor.roadrunner_sentry_mode")
    assert sentry_mode.state == STATE_ON
    assert sentry_mode.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.RUNNING
    assert sentry_mode.attributes[ATTR_ICON] == "mdi:cctv"

    tracker_state = hass.states.get("device_tracker.roadrunner")
    assert tracker_state.state == "not_home"
    assert tracker_state.attributes[ATTR_LATITUDE] == 37.123
    assert tracker_state.attributes[ATTR_LONGITUDE] == -122.456
    assert tracker_state.attributes[ATTR_GPS_ACCURACY] == 0
    assert tracker_state.attributes[ATTR_ICON] == "mdi:crosshairs-gps"

    battery_state = hass.states.get("sensor.roadrunner_battery")
    assert battery_state.state == "74"
    assert battery_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.BATTERY
    assert battery_state.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert battery_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE

    center_display_state = hass.states.get("sensor.roadrunner_center_display")
    assert center_display_state.state == "dog_mode"
    assert center_display_state.attributes[ATTR_ICON] == "mdi:television"
    assert center_display_state.attributes["raw_value"] == "8"

    charge_energy_added_state = hass.states.get("sensor.roadrunner_energy_added")
    assert charge_energy_added_state.state == "12.3"
    assert (
        charge_energy_added_state.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.ENERGY
    )
    assert (
        charge_energy_added_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.TOTAL_INCREASING
    )
    assert (
        charge_energy_added_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfEnergy.KILO_WATT_HOUR
    )
    assert entity_registry.async_get(
        "sensor.roadrunner_energy_added"
    ).options["sensor"]["suggested_display_precision"] == 1

    charge_limit_soc_state = hass.states.get("sensor.roadrunner_charge_limit")
    assert charge_limit_soc_state.state == "80"
    assert charge_limit_soc_state.attributes[ATTR_ICON] == "mdi:battery-charging-90"
    assert (
        charge_limit_soc_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert charge_limit_soc_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE
    assert entity_registry.async_get("sensor.roadrunner_charge_limit").options[
        "sensor"
    ]["suggested_display_precision"] == 0

    charge_current_request_state = hass.states.get(
        "sensor.roadrunner_charge_current_request"
    )
    assert charge_current_request_state.state == "24"
    assert (
        charge_current_request_state.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.CURRENT
    )
    assert (
        charge_current_request_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        charge_current_request_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfElectricCurrent.AMPERE
    )
    assert entity_registry.async_get(
        "sensor.roadrunner_charge_current_request"
    ).options["sensor"]["suggested_display_precision"] == 0

    charge_current_request_max_state = hass.states.get(
        "sensor.roadrunner_charge_current_request_max"
    )
    assert charge_current_request_max_state.state == "48"
    assert (
        charge_current_request_max_state.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.CURRENT
    )
    assert (
        charge_current_request_max_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        charge_current_request_max_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfElectricCurrent.AMPERE
    )
    assert entity_registry.async_get(
        "sensor.roadrunner_charge_current_request_max"
    ).options["sensor"]["suggested_display_precision"] == 0

    charger_actual_current_state = hass.states.get("sensor.roadrunner_charger_current")
    assert charger_actual_current_state.state == "40"
    assert (
        charger_actual_current_state.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.CURRENT
    )
    assert (
        charger_actual_current_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        charger_actual_current_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfElectricCurrent.AMPERE
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_current").options[
        "sensor"
    ]["suggested_display_precision"] == 0

    charger_phases_state = hass.states.get("sensor.roadrunner_charger_phases")
    assert charger_phases_state.state == "3"
    assert charger_phases_state.attributes[ATTR_ICON] == "mdi:sine-wave"
    assert (
        charger_phases_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert charger_phases_state.attributes[ATTR_UNIT_OF_MEASUREMENT] == "phases"
    assert entity_registry.async_get("sensor.roadrunner_charger_phases").options[
        "sensor"
    ]["suggested_display_precision"] == 0

    charger_power_state = hass.states.get("sensor.roadrunner_charger_power")
    assert charger_power_state.state == "11"
    assert charger_power_state.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.POWER
    assert (
        charger_power_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        charger_power_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfPower.KILO_WATT
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_power").options[
        "sensor"
    ]["suggested_display_precision"] == 0

    charger_voltage_state = hass.states.get("sensor.roadrunner_charger_voltage")
    assert charger_voltage_state.state == "240"
    assert (
        charger_voltage_state.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.VOLTAGE
    )
    assert (
        charger_voltage_state.attributes[ATTR_STATE_CLASS]
        == SensorStateClass.MEASUREMENT
    )
    assert (
        charger_voltage_state.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == UnitOfElectricPotential.VOLT
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_voltage").options[
        "sensor"
    ]["suggested_display_precision"] == 0

    charging_state = hass.states.get("sensor.roadrunner_charging_state")
    assert charging_state.state == "No Power"
    assert charging_state.attributes[ATTR_ICON] == "mdi:ev-station"

    climate_keeper = hass.states.get("sensor.roadrunner_climate_keeper")
    assert climate_keeper.state == "Dog"
    assert climate_keeper.attributes[ATTR_ICON] == "mdi:air-conditioner"

    elevation = hass.states.get("sensor.roadrunner_elevation")
    assert elevation.state == "123.0"
    assert elevation.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert elevation.attributes[ATTR_ICON] == "mdi:image-filter-hdr"
    assert elevation.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert elevation.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.METERS
    assert entity_registry.async_get("sensor.roadrunner_elevation").options[
        "sensor"
    ]["suggested_display_precision"] == 0

    exterior_color = hass.states.get("sensor.roadrunner_exterior_color")
    assert exterior_color.state == "Deep Blue"
    assert exterior_color.attributes[ATTR_ICON] == "mdi:format-color-fill"

    geofence = hass.states.get("sensor.roadrunner_geofence")
    assert geofence.state == "Home"
    assert geofence.attributes[ATTR_ICON] == "mdi:earth"

    heading = hass.states.get("sensor.roadrunner_heading")
    assert heading.state == "270"
    assert heading.attributes[ATTR_ICON] == "mdi:compass"
    assert heading.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert heading.attributes[ATTR_UNIT_OF_MEASUREMENT] == DEGREE
    assert entity_registry.async_get("sensor.roadrunner_heading").options["sensor"][
        "suggested_display_precision"
    ] == 0

    inside_temp = hass.states.get("sensor.roadrunner_temperature_inside")
    assert inside_temp.state == "22.4"
    assert inside_temp.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.TEMPERATURE
    assert inside_temp.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert inside_temp.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTemperature.CELSIUS
    assert entity_registry.async_get("sensor.roadrunner_temperature_inside").options[
        "sensor"
    ]["suggested_display_precision"] == 1

    outside_temp = hass.states.get("sensor.roadrunner_temperature_outside")
    assert outside_temp.state == "18.7"
    assert outside_temp.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.TEMPERATURE
    assert outside_temp.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert outside_temp.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTemperature.CELSIUS
    assert entity_registry.async_get("sensor.roadrunner_temperature_outside").options[
        "sensor"
    ]["suggested_display_precision"] == 1

    odometer = hass.states.get("sensor.roadrunner_odometer")
    assert odometer.state == "12345.6"
    assert odometer.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert odometer.attributes[ATTR_ICON] == "mdi:counter"
    assert odometer.attributes[ATTR_STATE_CLASS] == SensorStateClass.TOTAL_INCREASING
    assert odometer.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.KILOMETERS
    assert entity_registry.async_get("sensor.roadrunner_odometer").options["sensor"][
        "suggested_display_precision"
    ] == 0

    power = hass.states.get("sensor.roadrunner_power")
    assert power.state == "-7"
    assert power.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.POWER
    assert power.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert power.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfPower.KILO_WATT
    assert entity_registry.async_get("sensor.roadrunner_power").options["sensor"][
        "suggested_display_precision"
    ] == 0

    estimated_range = hass.states.get("sensor.roadrunner_range_estimated")
    assert estimated_range.state == "321.5"
    assert estimated_range.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert estimated_range.attributes[ATTR_ICON] == "mdi:map-marker-distance"
    assert estimated_range.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert estimated_range.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.KILOMETERS
    assert entity_registry.async_get("sensor.roadrunner_range_estimated").options[
        "sensor"
    ]["suggested_display_precision"] == 0

    ideal_range = hass.states.get("sensor.roadrunner_range_ideal")
    assert ideal_range.state == "330.1"
    assert ideal_range.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert ideal_range.attributes[ATTR_ICON] == "mdi:map-marker-distance"
    assert ideal_range.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert ideal_range.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.KILOMETERS
    assert entity_registry.async_get("sensor.roadrunner_range_ideal").options[
        "sensor"
    ]["suggested_display_precision"] == 0

    rated_range = hass.states.get("sensor.roadrunner_range_rated")
    assert rated_range.state == "325.7"
    assert rated_range.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.DISTANCE
    assert rated_range.attributes[ATTR_ICON] == "mdi:map-marker-distance"
    assert rated_range.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert rated_range.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfLength.KILOMETERS
    assert entity_registry.async_get("sensor.roadrunner_range_rated").options["sensor"][
        "suggested_display_precision"
    ] == 0

    scheduled_start_time = hass.states.get(
        "sensor.roadrunner_charging_start_time"
    )
    assert scheduled_start_time.state == "2026-06-07T12:34:56+00:00"
    assert (
        scheduled_start_time.attributes[ATTR_DEVICE_CLASS]
        == SensorDeviceClass.TIMESTAMP
    )

    shift_state = hass.states.get("sensor.roadrunner_shift_state")
    assert shift_state.state == "D"
    assert shift_state.attributes[ATTR_ICON] == "mdi:car-shift-pattern"

    since = hass.states.get("sensor.roadrunner_last_seen")
    assert since.state == "2026-06-07T12:00:00+00:00"
    assert since.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.TIMESTAMP
    assert since.attributes[ATTR_ICON] == "mdi:timer-sand"

    speed = hass.states.get("sensor.roadrunner_speed")
    assert speed.state == "88.0"
    assert speed.attributes[ATTR_DEVICE_CLASS] == SensorDeviceClass.SPEED
    assert speed.attributes[ATTR_ICON] == "mdi:speedometer"
    assert speed.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
    assert speed.attributes[ATTR_UNIT_OF_MEASUREMENT] == UnitOfSpeed.KILOMETERS_PER_HOUR
    assert entity_registry.async_get("sensor.roadrunner_speed").options["sensor"][
        "suggested_display_precision"
    ] == 0

    spoiler_type = hass.states.get("sensor.roadrunner_spoiler_type")
    assert spoiler_type.state == "CarbonFiber"
    assert spoiler_type.attributes[ATTR_ICON] == "mdi:weather-windy"

    assert hass.states.get("sensor.roadrunner_version").state == "2026.14.1"
    assert (
        hass.states.get("sensor.roadrunner_version").attributes[ATTR_ICON]
        == "mdi:numeric"
    )

    device = device_registry.async_get_device(
        identifiers={(DOMAIN, "teslamate/cars/1")}
    )
    assert device is not None
    assert device.manufacturer == "Tesla"
    assert device.name == "Roadrunner"
    assert device.model == "Model 3 Performance"
    assert device.sw_version == "2026.14.1"

    assert entity_registry.async_get(
        "binary_sensor.roadrunner_charge_port"
    ).unique_id == "teslamate/cars/1/charge_port_door_open"
    assert entity_registry.async_get("binary_sensor.roadrunner_doors").unique_id == (
        "teslamate/cars/1/doors_open"
    )
    assert entity_registry.async_get(
        "binary_sensor.roadrunner_door_driver_front"
    ).unique_id == "teslamate/cars/1/driver_front_door_open"
    assert entity_registry.async_get(
        "binary_sensor.roadrunner_door_driver_rear"
    ).unique_id == "teslamate/cars/1/driver_rear_door_open"
    assert entity_registry.async_get(
        "binary_sensor.roadrunner_door_passenger_front"
    ).unique_id == "teslamate/cars/1/passenger_front_door_open"
    assert entity_registry.async_get(
        "binary_sensor.roadrunner_door_passenger_rear"
    ).unique_id == "teslamate/cars/1/passenger_rear_door_open"
    assert entity_registry.async_get("binary_sensor.roadrunner_frunk").unique_id == (
        "teslamate/cars/1/frunk_open"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_health").unique_id == (
        "teslamate/cars/1/healthy"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_climate").unique_id == (
        "teslamate/cars/1/is_climate_on"
    )
    assert entity_registry.async_get(
        "binary_sensor.roadrunner_preconditioning"
    ).unique_id == "teslamate/cars/1/is_preconditioning"
    assert entity_registry.async_get("binary_sensor.roadrunner_occupancy").unique_id == (
        "teslamate/cars/1/is_user_present"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_lock").unique_id == (
        "teslamate/cars/1/locked"
    )
    assert entity_registry.async_get("binary_sensor.roadrunner_plug").unique_id == (
        "teslamate/cars/1/plugged_in"
    )
    assert entity_registry.async_get(
        "binary_sensor.roadrunner_sentry_mode"
    ).unique_id == "teslamate/cars/1/sentry_mode"
    tracker_entry = entity_registry.async_get("device_tracker.roadrunner")
    assert tracker_entry.unique_id == "teslamate/cars/1/location"
    assert tracker_entry.entity_category is None
    assert entity_registry.async_get("sensor.roadrunner_battery").unique_id == (
        "teslamate/cars/1/battery_level"
    )
    assert entity_registry.async_get("sensor.roadrunner_center_display").unique_id == (
        "teslamate/cars/1/center_display_state"
    )
    assert entity_registry.async_get("sensor.roadrunner_energy_added").unique_id == (
        "teslamate/cars/1/charge_energy_added"
    )
    assert entity_registry.async_get("sensor.roadrunner_charge_limit").unique_id == (
        "teslamate/cars/1/charge_limit_soc"
    )
    assert entity_registry.async_get(
        "sensor.roadrunner_charge_current_request"
    ).unique_id == "teslamate/cars/1/charge_current_request"
    assert entity_registry.async_get(
        "sensor.roadrunner_charge_current_request_max"
    ).unique_id == "teslamate/cars/1/charge_current_request_max"
    assert entity_registry.async_get("sensor.roadrunner_charger_current").unique_id == (
        "teslamate/cars/1/charger_actual_current"
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_phases").unique_id == (
        "teslamate/cars/1/charger_phases"
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_power").unique_id == (
        "teslamate/cars/1/charger_power"
    )
    assert entity_registry.async_get("sensor.roadrunner_charger_voltage").unique_id == (
        "teslamate/cars/1/charger_voltage"
    )
    assert entity_registry.async_get("sensor.roadrunner_charging_state").unique_id == (
        "teslamate/cars/1/charging_state"
    )
    assert entity_registry.async_get("sensor.roadrunner_climate_keeper").unique_id == (
        "teslamate/cars/1/climate_keeper_mode"
    )
    assert entity_registry.async_get("sensor.roadrunner_display_name") is None
    assert entity_registry.async_get("sensor.roadrunner_elevation").unique_id == (
        "teslamate/cars/1/elevation"
    )
    assert entity_registry.async_get("sensor.roadrunner_exterior_color").unique_id == (
        "teslamate/cars/1/exterior_color"
    )
    assert entity_registry.async_get("sensor.roadrunner_geofence").unique_id == (
        "teslamate/cars/1/geofence"
    )
    assert entity_registry.async_get("sensor.roadrunner_heading").unique_id == (
        "teslamate/cars/1/heading"
    )
    assert entity_registry.async_get(
        "sensor.roadrunner_temperature_inside"
    ).unique_id == "teslamate/cars/1/inside_temp"
    assert entity_registry.async_get(
        "sensor.roadrunner_temperature_outside"
    ).unique_id == "teslamate/cars/1/outside_temp"
    assert entity_registry.async_get("sensor.roadrunner_odometer").unique_id == (
        "teslamate/cars/1/odometer"
    )
    assert entity_registry.async_get("sensor.roadrunner_power").unique_id == (
        "teslamate/cars/1/power"
    )
    assert entity_registry.async_get("sensor.roadrunner_range_estimated").unique_id == (
        "teslamate/cars/1/est_battery_range_km"
    )
    assert entity_registry.async_get("sensor.roadrunner_range_ideal").unique_id == (
        "teslamate/cars/1/ideal_battery_range_km"
    )
    assert entity_registry.async_get("sensor.roadrunner_range_rated").unique_id == (
        "teslamate/cars/1/rated_battery_range_km"
    )
    assert entity_registry.async_get(
        "sensor.roadrunner_charging_start_time"
    ).unique_id == "teslamate/cars/1/scheduled_charging_start_time"
    assert entity_registry.async_get("sensor.roadrunner_shift_state").unique_id == (
        "teslamate/cars/1/shift_state"
    )
    assert entity_registry.async_get("sensor.roadrunner_last_seen").unique_id == (
        "teslamate/cars/1/since"
    )
    assert entity_registry.async_get("sensor.roadrunner_speed").unique_id == (
        "teslamate/cars/1/speed"
    )
    assert entity_registry.async_get("sensor.roadrunner_spoiler_type").unique_id == (
        "teslamate/cars/1/spoiler_type"
    )
    assert entity_registry.async_get("sensor.roadrunner_version").unique_id == (
        "teslamate/cars/1/version"
    )
    assert entry.title == "Roadrunner"

    async_fire_mqtt_message(hass, "teslamate/cars/1/doors_open", "false")
    async_fire_mqtt_message(hass, "teslamate/cars/1/display_name", "Bluebird")
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.roadrunner_doors").state == STATE_OFF
    assert hass.states.get("sensor.roadrunner_display_name") is None
    assert entry.title == "Bluebird"
    assert device_registry.async_get_device(
        identifiers={(DOMAIN, "teslamate/cars/1")}
    ).name == "Bluebird"

    async_fire_mqtt_message(hass, "teslamate/cars/1/charge_energy_added", "1.1")
    await hass.async_block_till_done()

    assert hass.states.get("sensor.roadrunner_energy_added").state == "1.1"


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("Charging", "Charging", id="single_word"),
        pytest.param("NoPower", "No Power", id="camel_case"),
    ],
)
async def test_charging_state_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test charging state value formatting."""
    await _async_setup_entry(hass)

    async_fire_mqtt_message(hass, "teslamate/cars/1/charging_state", payload)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.roadrunner_charging_state").state == state


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("off", "Off", id="lowercase"),
        pytest.param("DOG", "Dog", id="uppercase"),
    ],
)
async def test_climate_keeper_mode_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test climate keeper mode value formatting."""
    await _async_setup_entry(hass)

    async_fire_mqtt_message(hass, "teslamate/cars/1/climate_keeper_mode", payload)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.roadrunner_climate_keeper").state == state


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("true", STATE_OFF, id="healthy"),
        pytest.param("false", STATE_ON, id="problem"),
    ],
)
async def test_health_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test health value mapping."""
    await _async_setup_entry(hass)

    async_fire_mqtt_message(hass, "teslamate/cars/1/healthy", payload)
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.roadrunner_health").state == state


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("true", STATE_OFF, id="locked"),
        pytest.param("false", STATE_ON, id="unlocked"),
    ],
)
async def test_locked_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test locked value mapping."""
    await _async_setup_entry(hass)

    async_fire_mqtt_message(hass, "teslamate/cars/1/locked", payload)
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.roadrunner_lock").state == state


@pytest.mark.parametrize(
    ("payload", "state"),
    [
        pytest.param("0", "off", id="off"),
        pytest.param("2", "standby", id="standby"),
        pytest.param("3", "charging", id="charging"),
        pytest.param("4", "on", id="on"),
        pytest.param("5", "large_charging", id="large_charging"),
        pytest.param("6", "ready_to_unlock", id="ready_to_unlock"),
        pytest.param("7", "sentry_mode", id="sentry_mode"),
        pytest.param("8", "dog_mode", id="dog_mode"),
        pytest.param("9", "media", id="media"),
    ],
)
async def test_center_display_state_values(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, payload: str, state: str
) -> None:
    """Test center display state value mapping."""
    await _async_setup_entry(hass)

    async_fire_mqtt_message(hass, "teslamate/cars/1/center_display_state", payload)
    await hass.async_block_till_done()

    center_display_state = hass.states.get("sensor.roadrunner_center_display")
    assert center_display_state.state == state
    assert center_display_state.attributes["raw_value"] == payload


async def test_center_display_state_undocumented_value(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient, caplog: pytest.LogCaptureFixture
) -> None:
    """Test undocumented center display state value."""
    await _async_setup_entry(hass)
    caplog.set_level(logging.WARNING)

    async_fire_mqtt_message(hass, "teslamate/cars/1/center_display_state", "1")
    await hass.async_block_till_done()

    center_display_state = hass.states.get("sensor.roadrunner_center_display")
    assert center_display_state.state == STATE_UNKNOWN
    assert center_display_state.attributes["raw_value"] == "1"
    assert "Unexpected center display state value" not in caplog.text


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param("10", id="unmapped_integer"),
        pytest.param("bogus", id="non_integer"),
    ],
)
async def test_center_display_state_unexpected_value(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    caplog: pytest.LogCaptureFixture,
    payload: str,
) -> None:
    """Test unexpected center display state values."""
    await _async_setup_entry(hass)
    caplog.set_level(logging.WARNING)

    async_fire_mqtt_message(hass, "teslamate/cars/1/center_display_state", payload)
    await hass.async_block_till_done()

    center_display_state = hass.states.get("sensor.roadrunner_center_display")
    assert center_display_state.state == STATE_UNKNOWN
    assert center_display_state.attributes["raw_value"] == payload
    assert f"Unexpected center display state value: {payload}" in caplog.text


async def test_setup_fails_without_display_name(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test setup is retried when the display name topic is not retained."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Roadrunner",
        data={CONF_TOPIC_ROOT: "teslamate/cars/1"},
        unique_id="teslamate/cars/1",
    )
    entry.add_to_hass(hass)

    with patch("homeassistant.components.teslamate_mqtt.DISPLAY_NAME_TIMEOUT", 0):
        with patch(
            "homeassistant.components.teslamate_mqtt.mqtt.async_on_subscribe_done",
            side_effect=_async_on_subscribe_done,
        ):
            setup_task = hass.async_create_task(
                hass.config_entries.async_setup(entry.entry_id)
            )
            await asyncio.sleep(0)
        assert not await setup_task


async def test_setup_retries_when_mqtt_disconnected(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test setup is retried when the MQTT client is not connected."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Roadrunner",
        data={CONF_TOPIC_ROOT: "teslamate/cars/1"},
        unique_id="teslamate/cars/1",
    )
    entry.add_to_hass(hass)

    with patch(
        "homeassistant.components.teslamate_mqtt.mqtt.is_connected",
        return_value=False,
    ):
        assert not await hass.config_entries.async_setup(entry.entry_id)
