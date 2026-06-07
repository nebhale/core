"""Binary sensor platform for TeslaMate MQTT."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TeslaMateMqttConfigEntry
from .const import (
    TOPIC_CHARGE_PORT_DOOR_OPEN,
    TOPIC_DOORS_OPEN,
    TOPIC_DRIVER_FRONT_DOOR_OPEN,
    TOPIC_DRIVER_REAR_DOOR_OPEN,
    TOPIC_FRUNK_OPEN,
    TOPIC_HEALTHY,
    TOPIC_PASSENGER_FRONT_DOOR_OPEN,
    TOPIC_PASSENGER_REAR_DOOR_OPEN,
)
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
            TeslaMateDriverFrontDoorOpenBinarySensor(entry.runtime_data),
            TeslaMateDriverRearDoorOpenBinarySensor(entry.runtime_data),
            TeslaMatePassengerFrontDoorOpenBinarySensor(entry.runtime_data),
            TeslaMatePassengerRearDoorOpenBinarySensor(entry.runtime_data),
            TeslaMateFrunkOpenBinarySensor(entry.runtime_data),
            TeslaMateHealthyBinarySensor(entry.runtime_data),
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


class TeslaMateDoorOpenBinarySensor(TeslaMateMqttEntity, BinarySensorEntity):
    """Base class for TeslaMate door binary sensors."""

    _attr_device_class = BinarySensorDeviceClass.DOOR
    _attr_icon = "mdi:car-door"

    @property
    def is_on(self) -> bool | None:
        """Return true if the door is open."""
        if (value := self.data.value(self.key)) is None:
            return None
        return value.lower() == "true"


class TeslaMateDoorsOpenBinarySensor(TeslaMateDoorOpenBinarySensor):
    """Representation of whether any Tesla door is open."""

    _attr_name = "Doors"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_DOORS_OPEN)


class TeslaMateDriverFrontDoorOpenBinarySensor(TeslaMateDoorOpenBinarySensor):
    """Representation of whether the Tesla driver front door is open."""

    _attr_name = "Door (Driver Front)"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_DRIVER_FRONT_DOOR_OPEN)


class TeslaMateDriverRearDoorOpenBinarySensor(TeslaMateDoorOpenBinarySensor):
    """Representation of whether the Tesla driver rear door is open."""

    _attr_name = "Door (Driver Rear)"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_DRIVER_REAR_DOOR_OPEN)


class TeslaMatePassengerFrontDoorOpenBinarySensor(TeslaMateDoorOpenBinarySensor):
    """Representation of whether the Tesla passenger front door is open."""

    _attr_name = "Door (Passenger Front)"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_PASSENGER_FRONT_DOOR_OPEN)


class TeslaMatePassengerRearDoorOpenBinarySensor(TeslaMateDoorOpenBinarySensor):
    """Representation of whether the Tesla passenger rear door is open."""

    _attr_name = "Door (Passenger Rear)"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_PASSENGER_REAR_DOOR_OPEN)


class TeslaMateFrunkOpenBinarySensor(TeslaMateDoorOpenBinarySensor):
    """Representation of whether the Tesla frunk is open."""

    _attr_icon = "mdi:car"
    _attr_name = "Frunk"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_FRUNK_OPEN)


class TeslaMateHealthyBinarySensor(TeslaMateMqttEntity, BinarySensorEntity):
    """Representation of whether the Tesla has problems."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:heart-pulse"
    _attr_name = "Health"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_HEALTHY)

    @property
    def is_on(self) -> bool | None:
        """Return true if the Tesla has problems."""
        if (value := self.data.value(TOPIC_HEALTHY)) is None:
            return None
        return value.lower() == "false"
