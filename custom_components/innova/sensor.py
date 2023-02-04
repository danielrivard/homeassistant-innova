from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
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
    entities = [InnovaAmbientSensor(coordinator)]
    if coordinator.innova.supports_water_temp:
        entities.append(InnovaWaterSensor(coordinator))
    async_add_entities(entities)


class InnovaTemperatureSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: InnovaCoordinator) -> None:
        super().__init__(coordinator)
        self._innova = coordinator.innova
        self._device_info = InnovaDeviceInfo(self._innova)

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
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return self._device_info.device_info


class InnovaAmbientSensor(InnovaTemperatureSensor):
    def __init__(self, coordinator: InnovaCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def name(self) -> str | None:
        return f"{self._device_info.name}-{self.device_class}"

    @property
    def native_value(self) -> int:
        return self._innova.ambient_temp

    @property
    def unique_id(self) -> str | None:
        return f"{self._device_info.unique_id}-{self.device_class}"


class InnovaWaterSensor(InnovaTemperatureSensor):
    def __init__(self, coordinator: InnovaCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def name(self) -> str | None:
        return f"{self._device_info.name}-water-{self.device_class}"

    @property
    def native_value(self) -> int:
        return self._innova.water_temp

    @property
    def unique_id(self) -> str | None:
        return f"{self._device_info.unique_id}-water-{self.device_class}"
