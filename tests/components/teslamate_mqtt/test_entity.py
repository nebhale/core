"""Tests for TeslaMate MQTT entities."""

import asyncio
from collections.abc import Callable, Coroutine
from typing import Any
from unittest.mock import patch

from homeassistant.components import mqtt
from homeassistant.components.teslamate_mqtt.const import CONF_TOPIC_ROOT, DOMAIN
from homeassistant.const import (
    ATTR_GPS_ACCURACY,
    ATTR_ICON,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
)
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er

from tests.common import MockConfigEntry, async_fire_mqtt_message
from tests.typing import MqttMockHAClient


@callback
def _async_on_subscribe_done(
    hass: HomeAssistant,
    topic: str,
    qos: int,
    on_subscribe_status: Callable[[], None],
) -> CALLBACK_TYPE:
    """Call the MQTT subscribe status callback immediately."""
    on_subscribe_status()
    return lambda: None


async def _async_setup_entry(
    hass: HomeAssistant,
    topic_root: str = "teslamate/cars/1",
    display_name: str = "Roadrunner",
) -> MockConfigEntry:
    """Set up a TeslaMate MQTT config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=display_name,
        data={CONF_TOPIC_ROOT: topic_root},
        unique_id=topic_root,
    )
    entry.add_to_hass(hass)

    subscribe_started = asyncio.Event()
    real_async_subscribe = mqtt.async_subscribe

    async def async_subscribe(
        hass: HomeAssistant,
        topic: str,
        msg_callback: Callable[
            [mqtt.ReceiveMessage], Coroutine[Any, Any, None] | None
        ],
        qos: int = 0,
        encoding: str | None = "utf-8",
    ) -> CALLBACK_TYPE:
        """Subscribe to MQTT and mark the subscription as started."""
        unsub = await real_async_subscribe(hass, topic, msg_callback, qos, encoding)
        subscribe_started.set()
        return unsub

    with patch(
        "homeassistant.components.teslamate_mqtt.mqtt.async_on_subscribe_done",
        side_effect=_async_on_subscribe_done,
    ), patch(
        "homeassistant.components.teslamate_mqtt.mqtt.async_subscribe",
        side_effect=async_subscribe,
    ):
        setup_task = hass.async_create_task(
            hass.config_entries.async_setup(entry.entry_id)
        )
        await subscribe_started.wait()
        async_fire_mqtt_message(
            hass, f"{topic_root}/display_name", display_name, retain=True
        )
        assert await setup_task
    await hass.async_block_till_done()

    return entry


async def test_entities(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    entity_registry: er.EntityRegistry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test TeslaMate MQTT entities."""
    entry = await _async_setup_entry(hass)

    assert hass.states.get("binary_sensor.roadrunner_doors").state == STATE_UNKNOWN
    assert hass.states.get("device_tracker.roadrunner").state == STATE_UNKNOWN
    assert hass.states.get("sensor.roadrunner_version").state == STATE_UNKNOWN

    async_fire_mqtt_message(hass, "teslamate/cars/1/doors_open", "true")
    async_fire_mqtt_message(hass, "teslamate/cars/1/latitude", "37.123")
    async_fire_mqtt_message(hass, "teslamate/cars/1/longitude", "-122.456")
    async_fire_mqtt_message(hass, "teslamate/cars/1/version", "2026.14.1")
    async_fire_mqtt_message(hass, "teslamate/cars/1/model", "3")
    async_fire_mqtt_message(hass, "teslamate/cars/1/trim_badging", "Performance")
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.roadrunner_doors").state == STATE_ON
    assert (
        hass.states.get("binary_sensor.roadrunner_doors").attributes[ATTR_ICON]
        == "mdi:car-door"
    )

    tracker_state = hass.states.get("device_tracker.roadrunner")
    assert tracker_state.state == "not_home"
    assert tracker_state.attributes[ATTR_LATITUDE] == 37.123
    assert tracker_state.attributes[ATTR_LONGITUDE] == -122.456
    assert tracker_state.attributes[ATTR_GPS_ACCURACY] == 0
    assert tracker_state.attributes[ATTR_ICON] == "mdi:crosshairs-gps"

    assert hass.states.get("sensor.roadrunner_version").state == "2026.14.1"
    assert (
        hass.states.get("sensor.roadrunner_version").attributes[ATTR_ICON]
        == "mdi:numeric"
    )

    device = device_registry.async_get_device(identifiers={(DOMAIN, "teslamate/cars/1")})
    assert device is not None
    assert device.manufacturer == "Tesla"
    assert device.name == "Roadrunner"
    assert device.model == "Model 3 Performance"
    assert device.sw_version == "2026.14.1"

    assert entity_registry.async_get("binary_sensor.roadrunner_doors").unique_id == (
        "teslamate/cars/1/doors_open"
    )
    tracker_entry = entity_registry.async_get("device_tracker.roadrunner")
    assert tracker_entry.unique_id == "teslamate/cars/1/location"
    assert tracker_entry.entity_category is None
    assert entity_registry.async_get("sensor.roadrunner_version").unique_id == (
        "teslamate/cars/1/version"
    )
    assert entry.title == "Roadrunner"

    async_fire_mqtt_message(hass, "teslamate/cars/1/doors_open", "false")
    async_fire_mqtt_message(hass, "teslamate/cars/1/display_name", "Bluebird")
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.roadrunner_doors").state == STATE_OFF
    assert entry.title == "Bluebird"


async def test_setup_fails_without_display_name(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test setup is retried when the display name topic is not retained."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Roadrunner",
        data={CONF_TOPIC_ROOT: "teslamate/cars/1"},
        unique_id="teslamate/cars/1",
    )
    entry.add_to_hass(hass)

    with patch("homeassistant.components.teslamate_mqtt.DISPLAY_NAME_TIMEOUT", 0):
        with patch(
            "homeassistant.components.teslamate_mqtt.mqtt.async_on_subscribe_done",
            side_effect=_async_on_subscribe_done,
        ):
            setup_task = hass.async_create_task(
                hass.config_entries.async_setup(entry.entry_id)
            )
            await asyncio.sleep(0)
        assert not await setup_task


async def test_setup_retries_when_mqtt_disconnected(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test setup is retried when the MQTT client is not connected."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Roadrunner",
        data={CONF_TOPIC_ROOT: "teslamate/cars/1"},
        unique_id="teslamate/cars/1",
    )
    entry.add_to_hass(hass)

    with patch(
        "homeassistant.components.teslamate_mqtt.mqtt.is_connected",
        return_value=False,
    ):
        assert not await hass.config_entries.async_setup(entry.entry_id)
