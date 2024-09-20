"""The Innova component."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from innova_controls.innova import Innova
from .const import DEFAULT_SCAN_INTERVAL

from .const import DOMAIN
from .coordinator import InnovaCoordinator
from .options_flow import InnovaOptionsFlowHandler

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SENSOR, Platform.SWITCH]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Innova AC from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    host = entry.data[CONF_HOST]
    session = async_get_clientsession(hass)
    api = Innova(http_session=session, host=host)
    coordinator = create_coordinator(hass, api)

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


def create_coordinator(hass: HomeAssistant, api: Innova) -> InnovaCoordinator:
    # Use the update interval in seconds if set in hass.data, or default to DEFAULT_SCAN_INTERVAL
    update_interval_seconds = hass.data.get("innova_update_interval_seconds", DEFAULT_SCAN_INTERVAL)
    coordinator = InnovaCoordinator(
        hass,
        api,
        _LOGGER,
        name=DOMAIN,
        update_interval=timedelta(seconds=update_interval_seconds)
    )
    return coordinator
