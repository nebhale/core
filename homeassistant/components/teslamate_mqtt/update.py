"""Update platform for TeslaMate MQTT."""

from homeassistant.components.update import UpdateDeviceClass, UpdateEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TeslaMateMqttConfigEntry
from .const import TOPIC_UPDATE_AVAILABLE, TOPIC_UPDATE_VERSION, TOPIC_VERSION
from .entity import TeslaMateMqttEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TeslaMateMqttConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up TeslaMate MQTT update entities."""
    async_add_entities([TeslaMateUpdateEntity(entry.runtime_data)])


class TeslaMateUpdateEntity(TeslaMateMqttEntity, UpdateEntity):
    """Representation of a Tesla software update."""

    _attr_device_class = UpdateDeviceClass.FIRMWARE
    _attr_name = "Update"

    def __init__(self, data) -> None:
        """Initialize the update entity."""
        super().__init__(data, TOPIC_UPDATE_AVAILABLE)

    @property
    def installed_version(self) -> str | None:
        """Version installed and in use."""
        return self.data.value(TOPIC_VERSION)

    @property
    def latest_version(self) -> str | None:
        """Latest version available for install."""
        if (update_available := self.data.value(TOPIC_UPDATE_AVAILABLE)) is None:
            return None
        if update_available.lower() != "true":
            return self.installed_version
        return self.data.value(TOPIC_UPDATE_VERSION)
