"""The Hisense AEH-W4A1 integration."""

from __future__ import annotations

import logging

from pyaehw4a1.aehw4a1 import AehW4a1

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.CLIMATE]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hisense AEH-W4A1 from a config entry."""
    host = entry.data[CONF_HOST]
    try:
        ac = AehW4a1(host)
        await ac.check()
    except Exception as err:
        raise ConfigEntryNotReady(f"Cannot connect to {host}") from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = host

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
