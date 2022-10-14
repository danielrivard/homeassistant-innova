from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity,
                                             SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import InnovaCoordinator
from .device_info import InnovaDeviceInfo


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Add entities for passed config_entry in HA."""
    coordinator: InnovaCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([InnovaAmbientSensor(coordinator)])


class InnovaAmbientSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: InnovaCoordinator) -> None:
        self._innova = coordinator.innova
        self._device_info = InnovaDeviceInfo(self._innova)

    @property
    def name(self) -> str | None:
        return f"{self._device_info.name}-{self.device_class}"

    @property
    def state_class(self) -> SensorStateClass | str | None:
        return SensorStateClass.MEASUREMENT

    @property
    def device_class(self) -> SensorDeviceClass | str | None:
        return SensorDeviceClass.TEMPERATURE

    @property
    def native_unit_of_measurement(self) -> str | None:
        return TEMP_CELSIUS

    @property
    def native_value(self) -> int:
        return self._innova.ambient_temp

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return self._device_info.device_info

    @property
    def unique_id(self) -> str | None:
        return f"{self._innova.serial}-{self.device_class}"
