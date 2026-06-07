"""Tests for the TeslaMate MQTT config flow."""

from unittest.mock import patch

from homeassistant.components.teslamate_mqtt.const import CONF_TOPIC_ROOT, DOMAIN
from homeassistant.config_entries import SOURCE_MQTT, SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers.service_info.mqtt import MqttServiceInfo

from tests.common import MockConfigEntry
from tests.typing import MqttMockHAClient


async def test_mqtt_discovery(hass: HomeAssistant, mqtt_mock: MqttMockHAClient) -> None:
    """Test MQTT discovery creates a config entry."""
    discovery_info = MqttServiceInfo(
        topic="teslamate/cars/1/display_name",
        payload="Roadrunner",
        qos=0,
        retain=True,
        subscribed_topic="teslamate/cars/+/display_name",
        timestamp=0.0,
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_MQTT}, data=discovery_info
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Roadrunner"
    assert result["data"] == {CONF_TOPIC_ROOT: "teslamate/cars/1"}
    assert result["result"].unique_id == "teslamate/cars/1"


async def test_mqtt_discovery_namespaced_topic(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test MQTT discovery creates a config entry for a namespaced root."""
    discovery_info = MqttServiceInfo(
        topic="teslamate/home/cars/1/display_name",
        payload="Roadrunner",
        qos=0,
        retain=True,
        subscribed_topic="teslamate/+/cars/+/display_name",
        timestamp=0.0,
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_MQTT}, data=discovery_info
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {CONF_TOPIC_ROOT: "teslamate/home/cars/1"}
    assert result["result"].unique_id == "teslamate/home/cars/1"


async def test_mqtt_discovery_updates_existing_title(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test MQTT discovery updates the title for an existing config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Old Name",
        data={CONF_TOPIC_ROOT: "teslamate/cars/1"},
        unique_id="teslamate/cars/1",
    )
    entry.add_to_hass(hass)
    discovery_info = MqttServiceInfo(
        topic="teslamate/cars/1/display_name",
        payload="Roadrunner",
        qos=0,
        retain=True,
        subscribed_topic="teslamate/cars/+/display_name",
        timestamp=0.0,
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_MQTT}, data=discovery_info
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
    assert entry.title == "Roadrunner"


async def test_mqtt_discovery_invalid_topic(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test MQTT discovery aborts for invalid discovery data."""
    discovery_info = MqttServiceInfo(
        topic="teslamate/cars/1/version",
        payload="Roadrunner",
        qos=0,
        retain=True,
        subscribed_topic="teslamate/cars/+/display_name",
        timestamp=0.0,
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_MQTT}, data=discovery_info
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "invalid_discovery_info"


async def test_user_flow(hass: HomeAssistant, mqtt_mock: MqttMockHAClient) -> None:
    """Test manual configuration validates the display name topic."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM

    with patch(
        "homeassistant.components.teslamate_mqtt.config_flow._async_get_display_name",
        return_value="Roadrunner",
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_TOPIC_ROOT: "teslamate/cars/1"}
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Roadrunner"
    assert result["data"] == {CONF_TOPIC_ROOT: "teslamate/cars/1"}
    assert result["result"].unique_id == "teslamate/cars/1"


async def test_user_flow_no_display_name(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test manual configuration fails when display name is not retained."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    with patch(
        "homeassistant.components.teslamate_mqtt.config_flow._async_get_display_name",
        return_value=None,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_TOPIC_ROOT: "teslamate/cars/1"}
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "no_devices_found"}


async def test_user_flow_invalid_topic_root(
    hass: HomeAssistant, mqtt_mock: MqttMockHAClient
) -> None:
    """Test manual configuration rejects invalid topic roots."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_TOPIC_ROOT: "teslamate/cars/+"}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {CONF_TOPIC_ROOT: "invalid_topic_root"}
