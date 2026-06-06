"""Sensor platform for TeslaMate MQTT."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TeslaMateMqttConfigEntry
from .const import TOPIC_VERSION
from .entity import TeslaMateMqttEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TeslaMateMqttConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up TeslaMate MQTT sensors."""
    async_add_entities([TeslaMateVersionSensor(entry.runtime_data)])


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
