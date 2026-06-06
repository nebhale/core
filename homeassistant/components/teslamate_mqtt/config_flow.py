"""Config flow for the TeslaMate MQTT integration."""

import asyncio
from typing import Any

import voluptuous as vol

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.service_info.mqtt import MqttServiceInfo

from .const import CONF_TOPIC_ROOT, DOMAIN, TOPIC_DISPLAY_NAME

DISCOVERY_TOPICS = {
    "teslamate/cars/+/display_name",
    "teslamate/+/cars/+/display_name",
}
DISPLAY_NAME_TIMEOUT = 2


def _normalize_topic_root(topic_root: str) -> str:
    """Normalize a topic root."""
    return topic_root.strip().strip("/")


def _topic_root_from_display_name_topic(topic: str) -> str | None:
    """Return the topic root from a TeslaMate display name topic."""
    if not topic.endswith(f"/{TOPIC_DISPLAY_NAME}"):
        return None

    topic_root = topic.removesuffix(f"/{TOPIC_DISPLAY_NAME}")
    topic_parts = topic_root.split("/")

    if topic_parts[:2] == ["teslamate", "cars"] and len(topic_parts) == 3:
        return topic_root

    if (
        len(topic_parts) == 4
        and topic_parts[0] == "teslamate"
        and topic_parts[2] == "cars"
    ):
        return topic_root

    return None


async def _async_get_display_name(hass: HomeAssistant, topic_root: str) -> str | None:
    """Get the retained display name for a topic root."""
    event = asyncio.Event()
    display_name: str | None = None

    @callback
    def message_received(msg: mqtt.ReceiveMessage) -> None:
        nonlocal display_name
        if not isinstance(msg.payload, str) or not msg.payload:
            return
        display_name = msg.payload
        event.set()

    unsub = await mqtt.async_subscribe(
        hass, f"{topic_root}/{TOPIC_DISPLAY_NAME}", message_received
    )

    try:
        async with asyncio.timeout(DISPLAY_NAME_TIMEOUT):
            await event.wait()
    except TimeoutError:
        return None
    finally:
        unsub()

    return display_name


class TeslaMateMqttConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TeslaMate MQTT."""

    VERSION = 1

    async def async_step_mqtt(
        self, discovery_info: MqttServiceInfo
    ) -> ConfigFlowResult:
        """Handle a flow initialized by MQTT discovery."""
        if discovery_info.subscribed_topic not in DISCOVERY_TOPICS:
            return self.async_abort(reason="invalid_discovery_info")

        if not isinstance(discovery_info.payload, str) or not discovery_info.payload:
            return self.async_abort(reason="invalid_discovery_info")

        if (
            topic_root := _topic_root_from_display_name_topic(discovery_info.topic)
        ) is None:
            return self.async_abort(reason="invalid_discovery_info")

        existing_entry = await self.async_set_unique_id(topic_root)
        if existing_entry is not None:
            self.hass.config_entries.async_update_entry(
                existing_entry, title=discovery_info.payload
            )
            return self.async_abort(reason="already_configured")

        return self.async_create_entry(
            title=discovery_info.payload,
            data={CONF_TOPIC_ROOT: topic_root},
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            topic_root = _normalize_topic_root(user_input[CONF_TOPIC_ROOT])

            try:
                mqtt.valid_publish_topic(topic_root)
            except vol.Invalid:
                errors[CONF_TOPIC_ROOT] = "invalid_topic_root"
            else:
                await self.async_set_unique_id(topic_root)
                self._abort_if_unique_id_configured()

                if not await mqtt.async_wait_for_mqtt_client(self.hass):
                    errors["base"] = "mqtt_not_connected"
                elif (
                    display_name := await _async_get_display_name(self.hass, topic_root)
                ) is None:
                    errors["base"] = "no_devices_found"
                else:
                    return self.async_create_entry(
                        title=display_name,
                        data={CONF_TOPIC_ROOT: topic_root},
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_TOPIC_ROOT): cv.string},
            ),
            errors=errors,
        )
