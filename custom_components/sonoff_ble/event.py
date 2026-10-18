"""Event entities for Sonoff BLE buttons."""
from __future__ import annotations

from typing import Any

import homeassistant.helpers.device_registry as dr
from homeassistant.components.event import EventDeviceClass, EventEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DEVICE_BUTTONS, DOMAIN, SIGNAL_PRESS


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up an event entity for every button of the known devices."""
    entities: dict[tuple[str, str], SonoffBLEButtonEvent] = {}

    @callback
    def add_device(device_id: str, device_type: str) -> None:
        switches, actions = DEVICE_BUTTONS[device_type]
        new_entities = [
            SonoffBLEButtonEvent(device_id, switch, actions)
            for switch in switches
            if (device_id, switch) not in entities
        ]
        for entity in new_entities:
            entities[(device_id, entity.switch)] = entity
        if new_entities:
            async_add_entities(new_entities)

    # Devices are only discovered by a button press, restore the known ones
    device_registry = dr.async_get(hass)
    for device in dr.async_entries_for_config_entry(device_registry, entry.entry_id):
        if device.model not in DEVICE_BUTTONS:
            continue
        for domain, device_id in device.identifiers:
            if domain == DOMAIN:
                add_device(device_id, device.model)

    @callback
    def handle_press(device_info: dict[str, Any]) -> None:
        add_device(device_info["device_id"], device_info["device_type"])
        entity = entities.get((device_info["device_id"], device_info["switch"]))
        if entity:
            entity.press(device_info["action"])

    entry.async_on_unload(async_dispatcher_connect(hass, SIGNAL_PRESS, handle_press))


class SonoffBLEButtonEvent(EventEntity):
    """A button of a Sonoff BLE remote."""

    _attr_device_class = EventDeviceClass.BUTTON
    _attr_has_entity_name = True
    _attr_translation_key = "button"

    def __init__(self, device_id: str, switch: str, actions: list[str]) -> None:
        """Initialize the entity."""
        self.switch = switch
        self._added = False
        self._pending_action: str | None = None
        self._attr_unique_id = f"{device_id}_{switch}"
        self._attr_event_types = list(actions)
        self._attr_translation_placeholders = {"number": switch[1:]}
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, device_id)})

    async def async_added_to_hass(self) -> None:
        """Fire a press that arrived while the entity was being added."""
        await super().async_added_to_hass()
        self._added = True
        if self._pending_action:
            self.press(self._pending_action)
            self._pending_action = None

    @callback
    def press(self, action: str) -> None:
        """Handle a button press."""
        if not self._added:
            self._pending_action = action
            return
        self._trigger_event(action)
        self.async_write_ha_state()
