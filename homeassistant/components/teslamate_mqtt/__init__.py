"""The TeslaMate MQTT integration."""

import asyncio
from collections.abc import Callable
import logging
import re

from homeassistant.components import mqtt
from homeassistant.components.mqtt import ReceiveMessage
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv, device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    CONF_TOPIC_ROOT,
    DOMAIN,
    TOPIC_DISPLAY_NAME,
    TOPIC_MODEL,
    TOPIC_SPOILER_TYPE,
    TOPIC_TRIM_BADGING,
    TOPIC_VERSION,
    TOPIC_WHEEL_TYPE,
)

_LOGGER = logging.getLogger(__name__)

DISPLAY_NAME_TIMEOUT = 2
SUBSCRIBE_DONE_TIMEOUT = 10

_PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.SENSOR,
    Platform.UPDATE,
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

type TeslaMateMqttConfigEntry = ConfigEntry[TeslaMateMqttData]
type TeslaMateMqttListener = Callable[[], None]


def _split_camel_case(value: str) -> str:
    """Split camel-case words into space-separated words."""
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", value)


def _format_wheel_type(value: str) -> str:
    """Format a compact TeslaMate wheel type."""
    if (match := re.fullmatch(r"(?P<name>[A-Za-z]+)(?P<size>\d+)", value)) is None:
        return _split_camel_case(value)

    return f'{_split_camel_case(match["name"])} {match["size"]}"'


def _format_spoiler_type(value: str) -> str | None:
    """Format a compact TeslaMate spoiler type."""
    if value.lower() == "none":
        return None
    return _split_camel_case(value)


class TeslaMateMqttData:
    """TeslaMate MQTT state for one car."""

    def __init__(self, hass: HomeAssistant, entry: TeslaMateMqttConfigEntry) -> None:
        """Initialize TeslaMate MQTT data."""
        self.hass = hass
        self.entry = entry
        self.topic_root = entry.data[CONF_TOPIC_ROOT]
        self._listeners: list[TeslaMateMqttListener] = []
        self._unsub_mqtt: CALLBACK_TYPE | None = None
        self._values: dict[str, str] = {}
        self._display_name_seen = asyncio.Event()

    async def async_start(self) -> bool:
        """Start listening for TeslaMate MQTT messages."""
        topic = f"{self.topic_root}/#"
        subscribe_done = asyncio.Event()

        @callback
        def message_received(msg: ReceiveMessage) -> None:
            self._async_handle_message(msg.topic, msg.payload)

        unsub_subscribe_done = mqtt.async_on_subscribe_done(
            self.hass, topic, 0, subscribe_done.set
        )
        self._unsub_mqtt = await mqtt.async_subscribe(
            self.hass, topic, message_received
        )

        try:
            async with asyncio.timeout(SUBSCRIBE_DONE_TIMEOUT):
                await subscribe_done.wait()

            async with asyncio.timeout(DISPLAY_NAME_TIMEOUT):
                await self._display_name_seen.wait()
        except TimeoutError:
            return False
        finally:
            unsub_subscribe_done()

        return True

    async def async_stop(self) -> None:
        """Stop listening for TeslaMate MQTT messages."""
        if self._unsub_mqtt is not None:
            self._unsub_mqtt()
            self._unsub_mqtt = None

    @callback
    def async_add_listener(self, listener: TeslaMateMqttListener) -> CALLBACK_TYPE:
        """Add a listener for data updates."""
        self._listeners.append(listener)

        @callback
        def remove_listener() -> None:
            self._listeners.remove(listener)

        return remove_listener

    @callback
    def _async_handle_message(self, topic: str, payload: str | bytes | None) -> None:
        """Handle an incoming MQTT message."""
        if not topic.startswith(f"{self.topic_root}/"):
            return

        key = topic.removeprefix(f"{self.topic_root}/")
        if not isinstance(payload, str):
            return

        if key == TOPIC_DISPLAY_NAME:
            self.hass.config_entries.async_update_entry(self.entry, title=payload)
            self._display_name_seen.set()

        self._values[key] = payload

        if key in {
            TOPIC_DISPLAY_NAME,
            TOPIC_MODEL,
            TOPIC_SPOILER_TYPE,
            TOPIC_TRIM_BADGING,
            TOPIC_VERSION,
            TOPIC_WHEEL_TYPE,
        }:
            self._async_update_device_info()

        for listener in self._listeners:
            listener()

    @callback
    def _async_update_device_info(self) -> None:
        """Update device info for the car."""
        dr.async_get(self.hass).async_get_or_create(
            config_entry_id=self.entry.entry_id,
            **self.device_info,
        )

    def value(self, key: str) -> str | None:
        """Return the stored value for a TeslaMate topic key."""
        return self._values.get(key)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the car."""
        device_info = DeviceInfo(
            identifiers={(DOMAIN, self.topic_root)},
            manufacturer="Tesla",
            name=self.entry.title,
            sw_version=self.value(TOPIC_VERSION),
        )

        if model := self.model_name:
            device_info["model"] = model

        return device_info

    @property
    def model_name(self) -> str | None:
        """Return the formatted Tesla model name."""
        parts = [
            part
            for part in (self.value(TOPIC_MODEL), self.value(TOPIC_TRIM_BADGING))
            if part
        ]
        if not parts:
            return None

        model = f"Model {' '.join(parts)}"
        details = []
        if wheel_type := self.value(TOPIC_WHEEL_TYPE):
            details.append(f"{_format_wheel_type(wheel_type)} Wheels")
        if (spoiler_type := self.value(TOPIC_SPOILER_TYPE)) and (
            formatted_spoiler_type := _format_spoiler_type(spoiler_type)
        ):
            details.append(f"{formatted_spoiler_type} Spoiler")

        if details:
            return f"{model} ({', '.join(details)})"
        return model


async def async_setup_entry(
    hass: HomeAssistant, entry: TeslaMateMqttConfigEntry
) -> bool:
    """Set up TeslaMate MQTT from a config entry."""
    if not await mqtt.async_wait_for_mqtt_client(hass):
        _LOGGER.error("MQTT integration not available")
        raise ConfigEntryNotReady("MQTT integration not available")
    if not mqtt.is_connected(hass):
        raise ConfigEntryNotReady("MQTT client is not connected")

    entry.runtime_data = TeslaMateMqttData(hass, entry)
    if not await entry.runtime_data.async_start():
        await entry.runtime_data.async_stop()
        raise ConfigEntryNotReady(
            f"TeslaMate MQTT display name not available for {entry.runtime_data.topic_root}"
        )

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: TeslaMateMqttConfigEntry
) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
    if unload_ok:
        await entry.runtime_data.async_stop()

    return unload_ok
