"""Climate entity definition for Innova 2.0 HVAC."""
from __future__ import annotations

from homeassistant.components.climate import (ClimateEntity,
                                              ClimateEntityFeature, HVACAction,
                                              HVACMode)
from homeassistant.components.climate.const import (FAN_AUTO, FAN_HIGH,
                                                    FAN_LOW, FAN_MEDIUM,
                                                    PRESET_NONE, PRESET_SLEEP,
                                                    SWING_OFF, SWING_ON)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (ATTR_TEMPERATURE, PRECISION_HALVES,
                                 PRECISION_TENTHS, PRECISION_WHOLE,
                                 TEMP_CELSIUS)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from innova_controls.fan_speed import FanSpeed
from innova_controls.mode import Mode

from .const import DOMAIN
from .coordinator import InnovaCoordinator
from .device_info import InnovaDeviceInfo

FAN_MAPPINGS = {
    FanSpeed.AUTO: FAN_AUTO,
    FanSpeed.LOW: FAN_LOW,
    FanSpeed.MEDIUM: FAN_MEDIUM,
    FanSpeed.HIGH: FAN_HIGH,
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Add entities for passed config_entry in HA."""
    coordinator: InnovaCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([InnovaEntity(coordinator)])


class InnovaEntity(CoordinatorEntity[InnovaCoordinator], ClimateEntity):
    """Representation of an Innova AC Unit controls."""

    def __init__(self, coordinator: InnovaCoordinator):
        """Initialize the thermostat."""
        super().__init__(coordinator)
        self._device_info = InnovaDeviceInfo(self.coordinator.innova)

    @property
    def supported_features(self):
        """Return the list of supported features."""
        features: int = 0

        if self.coordinator.innova.supports_target_temp:
            features |= ClimateEntityFeature.TARGET_TEMPERATURE
        if self.coordinator.innova.supports_swing:
            features |= ClimateEntityFeature.SWING_MODE
        if self.coordinator.innova.supports_fan:
            features |= ClimateEntityFeature.FAN_MODE
        if self.coordinator.innova.supports_preset:
            features |= ClimateEntityFeature.PRESET_MODE

        return features

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return self._device_info.device_info

    @property
    def icon(self) -> str | None:
        return "mdi:hvac"

    @property
    def name(self):
        """Return the name of the thermostat."""
        return self._device_info.name

    @property
    def unique_id(self):
        """Return the serial number of the system"""
        return self.coordinator.innova.serial

    @property
    def precision(self):
        """Return the precision of the system."""
        if self.coordinator.innova.temperature_step == 0.1:
            return PRECISION_TENTHS
        elif self.coordinator.innova.temperature_step == 0.5:
            return PRECISION_HALVES
        else:
            return PRECISION_WHOLE

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self) -> float:
        """Return the current temperature."""
        return self.coordinator.innova.ambient_temp

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self.coordinator.innova.target_temperature

    @property
    def target_temperature_step(self) -> float | None:
        """Return the temperature step by which it can be increased/decreased."""
        return self.coordinator.innova.temperature_step

    @property
    def min_temp(self) -> float:
        return self.coordinator.innova.min_temperature

    @property
    def max_temp(self) -> float:
        return self.coordinator.innova.max_temperature

    @property
    def hvac_action(self):
        """Return the current state of the thermostat."""
        if not self.coordinator.innova.power:
            return HVACAction.OFF

        mode = self.coordinator.innova.mode
        if mode.is_heating:
            if self.current_temperature < self.target_temperature:
                return HVACAction.HEATING
            else:
                return HVACAction.IDLE
        if mode.is_cooling:
            if self.current_temperature > self.target_temperature:
                return HVACAction.COOLING
            else:
                return HVACAction.IDLE
        if mode.is_dehumidifying:
            return HVACAction.DRYING
        if mode.is_fan_only:
            return HVACAction.FAN
        if mode.is_auto:
            if self.current_temperature > self.target_temperature + 1:
                return HVACAction.COOLING
            elif self.current_temperature < self.target_temperature - 1:
                return HVACAction.HEATING
            else:
                return HVACAction.IDLE
        return HVACAction.IDLE

    @property
    def hvac_mode(self):
        """Return the current state of the thermostat."""
        if not self.coordinator.innova.power:
            return HVACMode.OFF

        if self.coordinator.innova.mode.is_cooling:
            return HVACMode.COOL
        if self.coordinator.innova.mode.is_heating:
            return HVACMode.HEAT
        if self.coordinator.innova.mode.is_dehumidifying:
            return HVACMode.DRY
        if self.coordinator.innova.mode.is_fan_only:
            return HVACMode.FAN_ONLY
        if self.coordinator.innova.mode.is_auto:
            return HVACMode.HEAT_COOL
        return HVACMode.OFF

    @property
    def hvac_modes(self):
        """Return available HVAC modes."""
        modes = [HVACMode.OFF]
        mode: Mode
        for mode in self.coordinator.innova.supported_modes:
            if mode.is_cooling:
                modes.append(HVACMode.COOL)
            elif mode.is_heating:
                modes.append(HVACMode.HEAT)
            elif mode.is_dehumidifying:
                modes.append(HVACMode.DRY)
            elif mode.is_fan_only:
                modes.append(HVACMode.FAN_ONLY)
            elif mode.is_auto:
                modes.append(HVACMode.HEAT_COOL)
        return modes

    @property
    def preset_modes(self) -> list[str] | None:
        return [PRESET_NONE, PRESET_SLEEP]

    @property
    def preset_mode(self) -> str | None:
        if self.coordinator.innova.night_mode == True:
            return PRESET_SLEEP
        if self.coordinator.innova.night_mode == False:
            return PRESET_NONE
        return None

    @property
    def fan_modes(self) -> list[str] | None:
        modes = []
        for fan in self.coordinator.innova.supported_fan_speeds:
            modes.append(FAN_MAPPINGS[fan])
        return modes

    @property
    def fan_mode(self) -> str | None:
        current_mode = self.coordinator.innova.fan_speed
        if current_mode in FAN_MAPPINGS:
            return FAN_MAPPINGS[current_mode]
        return None

    @property
    def swing_modes(self) -> list[str] | None:
        return [SWING_OFF, SWING_ON]

    @property
    def swing_mode(self) -> str | None:
        if self.coordinator.innova.rotation:
            return SWING_ON
        else:
            return SWING_OFF

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        if hvac_mode == HVACMode.OFF:
            await self.coordinator.innova.power_off()
        if hvac_mode == HVACMode.COOL:
            await self.coordinator.innova.set_cooling()
        if hvac_mode == HVACMode.HEAT:
            await self.coordinator.innova.set_heating()
        if hvac_mode == HVACMode.DRY:
            await self.coordinator.innova.set_dehumidifying()
        if hvac_mode == HVACMode.FAN_ONLY:
            await self.coordinator.innova.set_fan_only()
        if hvac_mode == HVACMode.HEAT_COOL:
            await self.coordinator.innova.set_auto()
        self.coordinator.async_update_listeners()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if preset_mode == PRESET_SLEEP:
            await self.coordinator.innova.night_mode_on()
        if preset_mode == PRESET_NONE:
            await self.coordinator.innova.night_mode_off()
        self.coordinator.async_update_listeners()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        if fan_mode == FAN_AUTO:
            await self.coordinator.innova.set_fan_speed(FanSpeed.AUTO)
        if fan_mode == FAN_LOW:
            await self.coordinator.innova.set_fan_speed(FanSpeed.LOW)
        if fan_mode == FAN_MEDIUM:
            await self.coordinator.innova.set_fan_speed(FanSpeed.MEDIUM)
        if fan_mode == FAN_HIGH:
            await self.coordinator.innova.set_fan_speed(FanSpeed.HIGH)
        self.coordinator.async_update_listeners()

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        if swing_mode == SWING_ON:
            await self.coordinator.innova.rotation_on()
        if swing_mode == SWING_OFF:
            await self.coordinator.innova.rotation_off()
        self.coordinator.async_update_listeners()

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        await self.coordinator.innova.set_temperature(temperature)
        self.coordinator.async_update_listeners()
