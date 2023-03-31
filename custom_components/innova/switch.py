from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
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
    coordinator: InnovaCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = [InnovaSchedulingSwitch(coordinator)]
    if coordinator.innova.supports_keyboard_lock:
        entities.append(InnovaKeyboardLockSwitch(coordinator))
    async_add_entities(entities)


class InnovaBaseSwitch(CoordinatorEntity[InnovaCoordinator], SwitchEntity):
    _attr_device_class = SwitchDeviceClass.SWITCH
    _switch_name: str

    def __init__(self, coordinator: InnovaCoordinator) -> None:
        super().__init__(coordinator)
        self._device_info = InnovaDeviceInfo(self.coordinator.innova)

    @property
    def device_info(self) -> DeviceInfo:
        return self._device_info.device_info

    @property
    def name(self) -> str:
        return f"{self._device_info.name}-{self._switch_name}-{self.device_class}"

    @property
    def unique_id(self) -> str:
        return f"{self._device_info.unique_id}-{self._switch_name}-{self.device_class}"


class InnovaSchedulingSwitch(InnovaBaseSwitch):
    _switch_name = "scheduling"

    def __init__(self, coordinator: InnovaCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.innova.scheduling_mode

    async def async_turn_on(self) -> None:
        await self.coordinator.innova.set_scheduling_on()
        self.coordinator.async_update_listeners()

    async def async_turn_off(self) -> None:
        await self.coordinator.innova.set_scheduling_off()
        self.coordinator.async_update_listeners()


class InnovaKeyboardLockSwitch(InnovaBaseSwitch):
    _switch_name = "keyboard-lock"

    def __init__(self, coordinator: InnovaCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.innova.keyboard_locked

    async def async_turn_on(self) -> None:
        await self.coordinator.innova.lock_keyboard()
        self.coordinator.async_update_listeners()

    async def async_turn_off(self) -> None:
        await self.coordinator.innova.unlock_keyboard()
        self.coordinator.async_update_listeners()
