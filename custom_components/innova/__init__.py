"""The Innova component."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from innova_controls.innova import Innova

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .coordinator import InnovaCoordinator

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SENSOR, Platform.SWITCH]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Innova AC from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    host = entry.data[CONF_HOST]
    session = async_get_clientsession(hass)
    api = Innova(http_session=session, host=host)

    # Get the scan interval from options, falling back to the default
    coordinator = await _async_update_coordinator(hass, entry, api)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Listen for changes in options
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    host = entry.data[CONF_HOST]
    session = async_get_clientsession(hass)
    api = Innova(http_session=session, host=host)
    
    # Reinitialize the coordinator with updated options
    coordinator = hass.data[DOMAIN][entry.entry_id]
    scan_interval_seconds = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)
    scan_interval = timedelta(seconds=scan_interval_seconds)

    # Dynamically update the polling interval
    coordinator.update_interval = scan_interval

    # Trigger an immediate refresh of the entities
    await coordinator.async_refresh()

    # Unload the existing platforms
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Recreate entities by setting up platforms again
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def _async_update_coordinator(hass: HomeAssistant, entry: ConfigEntry, api: Innova):
    """Helper function to update the coordinator."""
    scan_interval_seconds = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)
    scan_interval = timedelta(seconds=scan_interval_seconds)

    coordinator = create_coordinator(hass, api, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    # Save the coordinator in hass.data
    hass.data[DOMAIN][entry.entry_id] = coordinator

    return coordinator


def create_coordinator(hass: HomeAssistant, api: Innova, scan_interval: timedelta) -> InnovaCoordinator:
    """Create the coordinator with the provided scan interval."""
    coordinator = InnovaCoordinator(
        hass,
        api,
        _LOGGER,
        name=DOMAIN,
        update_interval=scan_interval
    )

    return coordinator
