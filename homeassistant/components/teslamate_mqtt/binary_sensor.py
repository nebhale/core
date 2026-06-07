"""Binary sensor platform for TeslaMate MQTT."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import EntityCategory
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
    TOPIC_IS_CLIMATE_ON,
    TOPIC_IS_PRECONDITIONING,
    TOPIC_IS_USER_PRESENT,
    TOPIC_LOCKED,
    TOPIC_PASSENGER_FRONT_DOOR_OPEN,
    TOPIC_PASSENGER_REAR_DOOR_OPEN,
    TOPIC_PLUGGED_IN,
    TOPIC_SENTRY_MODE,
    TOPIC_TPMS_SOFT_WARNING_FL,
    TOPIC_TPMS_SOFT_WARNING_FR,
    TOPIC_TPMS_SOFT_WARNING_RL,
    TOPIC_TPMS_SOFT_WARNING_RR,
    TOPIC_TRUNK_OPEN,
    TOPIC_WINDOWS_OPEN,
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
            TeslaMateClimateOnBinarySensor(entry.runtime_data),
            TeslaMatePreconditioningBinarySensor(entry.runtime_data),
            TeslaMateUserPresentBinarySensor(entry.runtime_data),
            TeslaMateLockedBinarySensor(entry.runtime_data),
            TeslaMatePluggedInBinarySensor(entry.runtime_data),
            TeslaMateSentryModeBinarySensor(entry.runtime_data),
            TeslaMateTireSoftWarningFrontLeftBinarySensor(entry.runtime_data),
            TeslaMateTireSoftWarningFrontRightBinarySensor(entry.runtime_data),
            TeslaMateTireSoftWarningRearLeftBinarySensor(entry.runtime_data),
            TeslaMateTireSoftWarningRearRightBinarySensor(entry.runtime_data),
            TeslaMateTrunkOpenBinarySensor(entry.runtime_data),
            TeslaMateWindowsOpenBinarySensor(entry.runtime_data),
        ]
    )


class TeslaMateBooleanBinarySensor(TeslaMateMqttEntity, BinarySensorEntity):
    """Base class for TeslaMate boolean binary sensors."""

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if (value := self.data.value(self.key)) is None:
            return None
        return value.lower() == "true"


class TeslaMateChargePortDoorOpenBinarySensor(TeslaMateMqttEntity, BinarySensorEntity):
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


class TeslaMateDoorOpenBinarySensor(TeslaMateBooleanBinarySensor):
    """Base class for TeslaMate door binary sensors."""

    _attr_device_class = BinarySensorDeviceClass.DOOR
    _attr_icon = "mdi:car-door"


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


class TeslaMateTrunkOpenBinarySensor(TeslaMateDoorOpenBinarySensor):
    """Representation of whether the Tesla trunk is open."""

    _attr_icon = "mdi:car"
    _attr_name = "Trunk"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_TRUNK_OPEN)


class TeslaMateWindowsOpenBinarySensor(TeslaMateBooleanBinarySensor):
    """Representation of whether any Tesla window is open."""

    _attr_device_class = BinarySensorDeviceClass.WINDOW
    _attr_icon = "mdi:car-door"
    _attr_name = "Windows"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_WINDOWS_OPEN)


class TeslaMateHealthyBinarySensor(TeslaMateMqttEntity, BinarySensorEntity):
    """Representation of whether the Tesla has problems."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
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


class TeslaMateClimateOnBinarySensor(TeslaMateBooleanBinarySensor):
    """Representation of whether the Tesla climate is on."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_icon = "mdi:air-conditioner"
    _attr_name = "Climate"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_IS_CLIMATE_ON)


class TeslaMatePreconditioningBinarySensor(TeslaMateBooleanBinarySensor):
    """Representation of whether the Tesla is preconditioning."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_icon = "mdi:air-conditioner"
    _attr_name = "Preconditioning"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_IS_PRECONDITIONING)


class TeslaMateUserPresentBinarySensor(TeslaMateBooleanBinarySensor):
    """Representation of whether a user is present in the Tesla."""

    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY
    _attr_icon = "mdi:account"
    _attr_name = "Occupancy"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_IS_USER_PRESENT)


class TeslaMateLockedBinarySensor(TeslaMateMqttEntity, BinarySensorEntity):
    """Representation of whether the Tesla is unlocked."""

    _attr_device_class = BinarySensorDeviceClass.LOCK
    _attr_name = "Lock"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_LOCKED)

    @property
    def is_on(self) -> bool | None:
        """Return true if the Tesla is unlocked."""
        if (value := self.data.value(TOPIC_LOCKED)) is None:
            return None
        return value.lower() == "false"


class TeslaMatePluggedInBinarySensor(TeslaMateBooleanBinarySensor):
    """Representation of whether the Tesla is plugged in."""

    _attr_device_class = BinarySensorDeviceClass.PLUG
    _attr_name = "Plug"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_PLUGGED_IN)


class TeslaMateSentryModeBinarySensor(TeslaMateBooleanBinarySensor):
    """Representation of whether Sentry Mode is active."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_icon = "mdi:cctv"
    _attr_name = "Sentry Mode"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_SENTRY_MODE)


class TeslaMateTireSoftWarningBinarySensor(TeslaMateBooleanBinarySensor):
    """Base class for TeslaMate tire soft warning binary sensors."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:car-tire-alert"


class TeslaMateTireSoftWarningFrontLeftBinarySensor(
    TeslaMateTireSoftWarningBinarySensor
):
    """Representation of whether the Tesla front left tire is soft."""

    _attr_name = "Tire Soft (Front Left)"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_TPMS_SOFT_WARNING_FL)


class TeslaMateTireSoftWarningFrontRightBinarySensor(
    TeslaMateTireSoftWarningBinarySensor
):
    """Representation of whether the Tesla front right tire is soft."""

    _attr_name = "Tire Soft (Front Right)"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_TPMS_SOFT_WARNING_FR)


class TeslaMateTireSoftWarningRearLeftBinarySensor(
    TeslaMateTireSoftWarningBinarySensor
):
    """Representation of whether the Tesla rear left tire is soft."""

    _attr_name = "Tire Soft (Rear Left)"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_TPMS_SOFT_WARNING_RL)


class TeslaMateTireSoftWarningRearRightBinarySensor(
    TeslaMateTireSoftWarningBinarySensor
):
    """Representation of whether the Tesla rear right tire is soft."""

    _attr_name = "Tire Soft (Rear Right)"

    def __init__(self, data) -> None:
        """Initialize the binary sensor."""
        super().__init__(data, TOPIC_TPMS_SOFT_WARNING_RR)
