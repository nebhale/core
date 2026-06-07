"""Sensor platform for TeslaMate MQTT."""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TeslaMateMqttConfigEntry
from .const import TOPIC_BATTERY_LEVEL, TOPIC_CENTER_DISPLAY_STATE, TOPIC_VERSION
from .entity import TeslaMateMqttEntity

_LOGGER = logging.getLogger(__name__)

CENTER_DISPLAY_STATES = {
    0: "off",
    2: "standby",
    3: "charging",
    4: "on",
    5: "large_charging",
    6: "ready_to_unlock",
    7: "sentry_mode",
    8: "dog_mode",
    9: "media",
}

ATTR_RAW_VALUE = "raw_value"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TeslaMateMqttConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up TeslaMate MQTT sensors."""
    async_add_entities(
        [
            TeslaMateBatteryLevelSensor(entry.runtime_data),
            TeslaMateCenterDisplayStateSensor(entry.runtime_data),
            TeslaMateVersionSensor(entry.runtime_data),
        ]
    )


class TeslaMateBatteryLevelSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla battery level."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_name = "Battery"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_BATTERY_LEVEL)

    @property
    def native_value(self) -> int | None:
        """Return the battery level."""
        if (value := self.data.value(TOPIC_BATTERY_LEVEL)) is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None


class TeslaMateCenterDisplayStateSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla center display state."""

    _attr_icon = "mdi:television"
    _attr_name = "Center Display"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CENTER_DISPLAY_STATE)

    @property
    def native_value(self) -> str | None:
        """Return the center display state."""
        raw_value = self.data.value(TOPIC_CENTER_DISPLAY_STATE)
        if raw_value is None:
            return None
        try:
            value = int(raw_value)
        except ValueError:
            _LOGGER.warning("Unexpected center display state value: %s", raw_value)
            return None
        if value == 1:
            return None
        if (state := CENTER_DISPLAY_STATES.get(value)) is None:
            _LOGGER.warning("Unexpected center display state value: %s", raw_value)
            return None
        return state

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return extra state attributes."""
        if (raw_value := self.data.value(TOPIC_CENTER_DISPLAY_STATE)) is None:
            return {}
        return {ATTR_RAW_VALUE: raw_value}


class TeslaMateVersionSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla firmware version."""

    _attr_icon = "mdi:numeric"
    _attr_name = "Version"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_VERSION)

    @property
    def native_value(self) -> str | None:
        """Return the firmware version."""
        return self.data.value(TOPIC_VERSION)
