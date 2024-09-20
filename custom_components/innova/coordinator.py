import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
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
        """Initialize the Innova Coordinator."""
        self.innova = innova

        super().__init__(hass, logger, name=name, update_interval=update_interval)

    async def _async_update_data(self) -> Innova:
        """Fetch data from the API endpoint.

        This is the place to pre-process the data for lookup tables so entities can quickly look up their data.
        """
        success = await self.innova.async_update()
        if not success:
            raise UpdateFailed("Innova connection issue")
        
        return self.innova
