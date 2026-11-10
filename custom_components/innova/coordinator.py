import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from innova_controls.innova import Innova


class InnovaCoordinator(DataUpdateCoordinator[Innova]):
    def __init__(
        self,
        hass: HomeAssistant,
        innova: Innova,
        logger: logging.Logger,
        name: str,
        update_interval: timedelta,
    ):
        self.innova = innova

        super().__init__(hass, logger, name=name, update_interval=update_interval)

    async def _async_update_data(self) -> Innova:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        success = await self.innova.async_update()
        if not success:
            raise UpdateFailed("Innova connection issue")
        
        return self.innova

    def async_handle_command(self, success: bool) -> None:
        """Raise when the unit did not confirm a command, else update entities."""
        if not success:
            raise HomeAssistantError(f"Failed to send command to {self.innova.name}")
        self.async_update_listeners()
