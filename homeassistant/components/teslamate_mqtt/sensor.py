"""Sensor platform for TeslaMate MQTT."""

from datetime import datetime
import logging
import re

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    DEGREE,
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfLength,
    UnitOfPower,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

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
    TOPIC_CHARGING_STATE,
    TOPIC_CLIMATE_KEEPER_MODE,
    TOPIC_ELEVATION,
    TOPIC_EST_BATTERY_RANGE_KM,
    TOPIC_EXTERIOR_COLOR,
    TOPIC_GEOFENCE,
    TOPIC_HEADING,
    TOPIC_IDEAL_BATTERY_RANGE_KM,
    TOPIC_INSIDE_TEMP,
    TOPIC_ODOMETER,
    TOPIC_OUTSIDE_TEMP,
    TOPIC_POWER,
    TOPIC_RATED_BATTERY_RANGE_KM,
    TOPIC_SCHEDULED_CHARGING_START_TIME,
    TOPIC_SHIFT_STATE,
    TOPIC_SINCE,
    TOPIC_SPEED,
    TOPIC_STATE,
    TOPIC_TIME_TO_FULL_CHARGE,
    TOPIC_TPMS_PRESSURE_FL,
    TOPIC_TPMS_PRESSURE_FR,
    TOPIC_TPMS_PRESSURE_RL,
    TOPIC_TPMS_PRESSURE_RR,
    TOPIC_USABLE_BATTERY_LEVEL,
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


def _split_camel_case(value: str) -> str:
    """Split camel-case words into space-separated words."""
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", value)


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
            TeslaMateChargingStateSensor(entry.runtime_data),
            TeslaMateClimateKeeperModeSensor(entry.runtime_data),
            TeslaMateElevationSensor(entry.runtime_data),
            TeslaMateEstimatedBatteryRangeSensor(entry.runtime_data),
            TeslaMateExteriorColorSensor(entry.runtime_data),
            TeslaMateGeofenceSensor(entry.runtime_data),
            TeslaMateHeadingSensor(entry.runtime_data),
            TeslaMateIdealBatteryRangeSensor(entry.runtime_data),
            TeslaMateInsideTemperatureSensor(entry.runtime_data),
            TeslaMateOdometerSensor(entry.runtime_data),
            TeslaMateOutsideTemperatureSensor(entry.runtime_data),
            TeslaMatePowerSensor(entry.runtime_data),
            TeslaMateRatedBatteryRangeSensor(entry.runtime_data),
            TeslaMateScheduledChargingStartTimeSensor(entry.runtime_data),
            TeslaMateShiftStateSensor(entry.runtime_data),
            TeslaMateSinceSensor(entry.runtime_data),
            TeslaMateSpeedSensor(entry.runtime_data),
            TeslaMateStateSensor(entry.runtime_data),
            TeslaMateTimeToFullChargeSensor(entry.runtime_data),
            TeslaMateTirePressureFrontLeftSensor(entry.runtime_data),
            TeslaMateTirePressureFrontRightSensor(entry.runtime_data),
            TeslaMateTirePressureRearLeftSensor(entry.runtime_data),
            TeslaMateTirePressureRearRightSensor(entry.runtime_data),
            TeslaMateUsableBatteryLevelSensor(entry.runtime_data),
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


class TeslaMateUsableBatteryLevelSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla usable battery level."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_name = "Usable Battery"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_USABLE_BATTERY_LEVEL)

    @property
    def native_value(self) -> int | None:
        """Return the usable battery level."""
        if (value := self.data.value(TOPIC_USABLE_BATTERY_LEVEL)) is None:
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


class TeslaMateFloatSensor(TeslaMateMqttEntity, SensorEntity):
    """Base class for TeslaMate float sensors."""

    @property
    def native_value(self) -> float | None:
        """Return the float value."""
        if (value := self.data.value(self.key)) is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None


class TeslaMateDistanceSensor(TeslaMateFloatSensor):
    """Base class for TeslaMate distance sensors."""

    _attr_device_class = SensorDeviceClass.DISTANCE
    _attr_state_class = SensorStateClass.MEASUREMENT


class TeslaMatePowerSensor(TeslaMateIntegerMeasurementSensor):
    """Representation of the Tesla power."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_name = "Power"
    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_POWER)


class TeslaMateTemperatureSensor(TeslaMateFloatSensor):
    """Base class for TeslaMate temperature sensors."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1


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


class TeslaMateChargingStateSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla charging state."""

    _attr_icon = "mdi:ev-station"
    _attr_name = "Charging State"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CHARGING_STATE)

    @property
    def native_value(self) -> str | None:
        """Return the charging state."""
        if (value := self.data.value(TOPIC_CHARGING_STATE)) is None:
            return None
        return _split_camel_case(value)


class TeslaMateClimateKeeperModeSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla climate keeper mode."""

    _attr_icon = "mdi:air-conditioner"
    _attr_name = "Climate Keeper"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_CLIMATE_KEEPER_MODE)

    @property
    def native_value(self) -> str | None:
        """Return the climate keeper mode."""
        if (value := self.data.value(TOPIC_CLIMATE_KEEPER_MODE)) is None:
            return None
        return value.title()


class TeslaMateExteriorColorSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla exterior color."""

    _attr_icon = "mdi:format-color-fill"
    _attr_name = "Exterior Color"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_EXTERIOR_COLOR)

    @property
    def native_value(self) -> str | None:
        """Return the exterior color."""
        if (value := self.data.value(TOPIC_EXTERIOR_COLOR)) is None:
            return None
        return _split_camel_case(value)


class TeslaMateGeofenceSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla geofence."""

    _attr_icon = "mdi:earth"
    _attr_name = "Geofence"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_GEOFENCE)

    @property
    def native_value(self) -> str | None:
        """Return the geofence."""
        return self.data.value(TOPIC_GEOFENCE)


class TeslaMateHeadingSensor(TeslaMateIntegerMeasurementSensor):
    """Representation of the Tesla heading."""

    _attr_icon = "mdi:compass"
    _attr_name = "Heading"
    _attr_native_unit_of_measurement = DEGREE
    _attr_suggested_display_precision = 0

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_HEADING)


class TeslaMateElevationSensor(TeslaMateDistanceSensor):
    """Representation of the Tesla elevation."""

    _attr_icon = "mdi:image-filter-hdr"
    _attr_name = "Elevation"
    _attr_native_unit_of_measurement = UnitOfLength.METERS
    _attr_suggested_display_precision = 0

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_ELEVATION)


class TeslaMateBatteryRangeSensor(TeslaMateDistanceSensor):
    """Base class for TeslaMate battery range sensors."""

    _attr_icon = "mdi:map-marker-distance"
    _attr_native_unit_of_measurement = UnitOfLength.KILOMETERS
    _attr_suggested_display_precision = 0


class TeslaMateEstimatedBatteryRangeSensor(TeslaMateBatteryRangeSensor):
    """Representation of the Tesla estimated battery range."""

    _attr_name = "Range (Estimated)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_EST_BATTERY_RANGE_KM)


class TeslaMateIdealBatteryRangeSensor(TeslaMateBatteryRangeSensor):
    """Representation of the Tesla ideal battery range."""

    _attr_name = "Range (Ideal)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_IDEAL_BATTERY_RANGE_KM)


class TeslaMateOdometerSensor(TeslaMateDistanceSensor):
    """Representation of the Tesla odometer."""

    _attr_icon = "mdi:counter"
    _attr_name = "Odometer"
    _attr_native_unit_of_measurement = UnitOfLength.KILOMETERS
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_suggested_display_precision = 0

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_ODOMETER)


class TeslaMateInsideTemperatureSensor(TeslaMateTemperatureSensor):
    """Representation of the Tesla inside temperature."""

    _attr_name = "Temperature (Inside)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_INSIDE_TEMP)


class TeslaMateOutsideTemperatureSensor(TeslaMateTemperatureSensor):
    """Representation of the Tesla outside temperature."""

    _attr_name = "Temperature (Outside)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_OUTSIDE_TEMP)


class TeslaMateRatedBatteryRangeSensor(TeslaMateBatteryRangeSensor):
    """Representation of the Tesla rated battery range."""

    _attr_name = "Range (Rated)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_RATED_BATTERY_RANGE_KM)


class TeslaMateScheduledChargingStartTimeSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla scheduled charging start time."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_name = "Charging Start Time"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_SCHEDULED_CHARGING_START_TIME)

    @property
    def native_value(self) -> datetime | None:
        """Return the scheduled charging start time."""
        if (value := self.data.value(TOPIC_SCHEDULED_CHARGING_START_TIME)) is None:
            return None
        return dt_util.parse_datetime(value)


class TeslaMateShiftStateSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla shift state."""

    _attr_icon = "mdi:car-shift-pattern"
    _attr_name = "Shift State"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_SHIFT_STATE)

    @property
    def native_value(self) -> str | None:
        """Return the shift state."""
        return self.data.value(TOPIC_SHIFT_STATE)


class TeslaMateSinceSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of when TeslaMate last saw the Tesla."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:timer-sand"
    _attr_name = "Last Seen"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_SINCE)

    @property
    def native_value(self) -> datetime | None:
        """Return when TeslaMate last saw the Tesla."""
        if (value := self.data.value(TOPIC_SINCE)) is None:
            return None
        return dt_util.parse_datetime(value)


class TeslaMateSpeedSensor(TeslaMateFloatSensor):
    """Representation of the Tesla speed."""

    _attr_device_class = SensorDeviceClass.SPEED
    _attr_icon = "mdi:speedometer"
    _attr_name = "Speed"
    _attr_native_unit_of_measurement = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_SPEED)


class TeslaMateStateSensor(TeslaMateMqttEntity, SensorEntity):
    """Representation of the Tesla state."""

    _attr_icon = "mdi:car-connected"
    _attr_name = "State"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_STATE)

    @property
    def native_value(self) -> str | None:
        """Return the state."""
        if (value := self.data.value(TOPIC_STATE)) is None:
            return None
        return value.title()


class TeslaMateTimeToFullChargeSensor(TeslaMateFloatSensor):
    """Representation of the Tesla time to full charge."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_icon = "mdi:timer"
    _attr_name = "Charging Time Left"
    _attr_native_unit_of_measurement = UnitOfTime.HOURS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_TIME_TO_FULL_CHARGE)


class TeslaMateTirePressureSensor(TeslaMateFloatSensor):
    """Base class for TeslaMate tire pressure sensors."""

    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_icon = "mdi:gauge"
    _attr_native_unit_of_measurement = UnitOfPressure.BAR
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1


class TeslaMateTirePressureFrontLeftSensor(TeslaMateTirePressureSensor):
    """Representation of the Tesla front left tire pressure."""

    _attr_name = "Tire Pressure (Front Left)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_TPMS_PRESSURE_FL)


class TeslaMateTirePressureFrontRightSensor(TeslaMateTirePressureSensor):
    """Representation of the Tesla front right tire pressure."""

    _attr_name = "Tire Pressure (Front Right)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_TPMS_PRESSURE_FR)


class TeslaMateTirePressureRearLeftSensor(TeslaMateTirePressureSensor):
    """Representation of the Tesla rear left tire pressure."""

    _attr_name = "Tire Pressure (Rear Left)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_TPMS_PRESSURE_RL)


class TeslaMateTirePressureRearRightSensor(TeslaMateTirePressureSensor):
    """Representation of the Tesla rear right tire pressure."""

    _attr_name = "Tire Pressure (Rear Right)"

    def __init__(self, data) -> None:
        """Initialize the sensor."""
        super().__init__(data, TOPIC_TPMS_PRESSURE_RR)


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
