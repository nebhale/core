"""Device tracker platform for TeslaMate MQTT."""

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TeslaMateMqttConfigEntry
from .const import TOPIC_LATITUDE, TOPIC_LONGITUDE
from .entity import TeslaMateMqttEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TeslaMateMqttConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up TeslaMate MQTT device tracker."""
    async_add_entities([TeslaMateDeviceTracker(entry.runtime_data)])


class TeslaMateDeviceTracker(TeslaMateMqttEntity, TrackerEntity):
    """Representation of the Tesla location."""

    _attr_entity_category = None
    _attr_icon = "mdi:crosshairs-gps"
    _attr_name = None

    def __init__(self, data) -> None:
        """Initialize the device tracker."""
        super().__init__(data, "location")

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        if (value := self.data.value(TOPIC_LATITUDE)) is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        if (value := self.data.value(TOPIC_LONGITUDE)) is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @property
    def source_type(self) -> SourceType:
        """Return the source type."""
        return SourceType.GPS
