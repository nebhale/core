"""Binary sensor platform for TeslaMate MQTT."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TeslaMateMqttConfigEntry
from .const import TOPIC_CHARGE_PORT_DOOR_OPEN, TOPIC_DOORS_OPEN
from .entity import TeslaMateMqttEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TeslaMateMqttConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up TeslaMate MQTT binary sensors."""
    async_add_entities(
        [
            TeslaMateChargePortDoorOpenBinarySensor(entry.runtime_data),
            TeslaMateDoorsOpenBinarySensor(entry.runtime_data),
        ]
    )


class TeslaMateChargePortDoorOpenBinarySensor(
    TeslaMateMqttEntity, BinarySensorEntity
):
    """Representation of whether the Tesla charge port is open."""

    _attr_device_class = BinarySensorDeviceClass.DOOR
    _attr_icon = "mdi:ev-plug-tesla"
    _attr_name = "Charge Port"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_CHARGE_PORT_DOOR_OPEN)

    @property
    def is_on(self) -> bool | None:
        """Return true if the charge port is open."""
        if (value := self.data.value(TOPIC_CHARGE_PORT_DOOR_OPEN)) is None:
            return None
        return value.lower() == "true"


class TeslaMateDoorsOpenBinarySensor(TeslaMateMqttEntity, BinarySensorEntity):
    """Representation of whether any Tesla door is open."""

    _attr_device_class = BinarySensorDeviceClass.DOOR
    _attr_icon = "mdi:car-door"
    _attr_name = "Doors"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_DOORS_OPEN)

    @property
    def is_on(self) -> bool | None:
        """Return true if any door is open."""
        if (value := self.data.value(TOPIC_DOORS_OPEN)) is None:
            return None
        return value.lower() == "true"
