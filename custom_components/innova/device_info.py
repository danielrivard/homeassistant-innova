from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import DeviceInfo
from innova_controls.innova import Innova

from .const import DOMAIN, MANUFACTURER


class InnovaDeviceInfo:
    """Provide device info from the device, shared across platforms."""

    def __init__(self, innova: Innova) -> None:
        """Initialize the DeviceInfo."""
        self._innova = innova
        self._unique_id = self._innova.serial
        if not self._unique_id:
            self._unique_id = self._innova.uid

    @property
    def device_info(self) -> DeviceInfo:
        """Provides a device specific attributes."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._unique_id)},
            name=self._innova.name,
            connections={(CONNECTION_NETWORK_MAC, self._innova.uid)},
            manufacturer=MANUFACTURER,
            sw_version=self._innova.software_version,
            model=self._innova.model,
        )

    @property
    def name(self) -> str:
        return self._innova.name

    @property
    def unique_id(self) -> str:
        return self._unique_id
