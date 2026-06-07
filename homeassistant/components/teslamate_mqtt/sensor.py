"""Sensor platform for TeslaMate MQTT."""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TeslaMateMqttConfigEntry
from .const import (
    TOPIC_BATTERY_LEVEL,
    TOPIC_CENTER_DISPLAY_STATE,
    TOPIC_CHARGE_CURRENT_REQUEST,
    TOPIC_CHARGE_CURRENT_REQUEST_MAX,
    TOPIC_CHARGE_ENERGY_ADDED,
    TOPIC_CHARGE_LIMIT_SOC,
    TOPIC_CHARGER_ACTUAL_CURRENT,
    TOPIC_CHARGER_PHASES,
    TOPIC_CHARGER_POWER,
    TOPIC_CHARGER_VOLTAGE,
    TOPIC_VERSION,
)
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
            TeslaMateChargeEnergyAddedSensor(entry.runtime_data),
            TeslaMateChargeLimitSocSensor(entry.runtime_data),
            TeslaMateChargeCurrentRequestSensor(entry.runtime_data),
            TeslaMateChargeCurrentRequestMaxSensor(entry.runtime_data),
            TeslaMateChargerActualCurrentSensor(entry.runtime_data),
            TeslaMateChargerPhasesSensor(entry.runtime_data),
            TeslaMateChargerPowerSensor(entry.runtime_data),
            TeslaMateChargerVoltageSensor(entry.runtime_data),
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


class TeslaMateCurrentSensor(TeslaMateMqttEntity, SensorEntity):
    """Base class for TeslaMate current sensors."""

    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0

    @property
    def native_value(self) -> int | None:
        """Return the current."""
        if (value := self.data.value(self.key)) is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None


class TeslaMateIntegerMeasurementSensor(TeslaMateMqttEntity, SensorEntity):
    """Base class for TeslaMate integer measurement sensors."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0

    @property
    def native_value(self) -> int | None:
        """Return the integer measurement."""
        if (value := self.data.value(self.key)) is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None


class TeslaMateChargeCurrentRequestSensor(TeslaMateCurrentSensor):
    """Representation of the Tesla charge current request."""

    _attr_name = "Charge Current Request"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CHARGE_CURRENT_REQUEST)


class TeslaMateChargeCurrentRequestMaxSensor(TeslaMateCurrentSensor):
    """Representation of the Tesla maximum charge current request."""

    _attr_name = "Charge Current Request (Max)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CHARGE_CURRENT_REQUEST_MAX)


class TeslaMateChargerActualCurrentSensor(TeslaMateCurrentSensor):
    """Representation of the Tesla charger current."""

    _attr_name = "Charger Current"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CHARGER_ACTUAL_CURRENT)


class TeslaMateChargerPhasesSensor(TeslaMateIntegerMeasurementSensor):
    """Representation of the Tesla charger phases."""

    _attr_icon = "mdi:sine-wave"
    _attr_name = "Charger Phases"
    _attr_native_unit_of_measurement = "phases"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CHARGER_PHASES)


class TeslaMateChargerPowerSensor(TeslaMateIntegerMeasurementSensor):
    """Representation of the Tesla charger power."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_name = "Charger Power"
    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CHARGER_POWER)


class TeslaMateChargerVoltageSensor(TeslaMateIntegerMeasurementSensor):
    """Representation of the Tesla charger voltage."""

    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_name = "Charger Voltage"
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CHARGER_VOLTAGE)


class TeslaMateChargeEnergyAddedSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla charge energy added."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_name = "Energy Added"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_suggested_display_precision = 1

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CHARGE_ENERGY_ADDED)

    @property
    def native_value(self) -> float | None:
        """Return the charge energy added."""
        if (value := self.data.value(TOPIC_CHARGE_ENERGY_ADDED)) is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None


class TeslaMateChargeLimitSocSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla charge limit."""

    _attr_icon = "mdi:battery-charging-90"
    _attr_name = "Charge Limit"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CHARGE_LIMIT_SOC)

    @property
    def native_value(self) -> int | None:
        """Return the charge limit."""
        if (value := self.data.value(TOPIC_CHARGE_LIMIT_SOC)) is None:
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
