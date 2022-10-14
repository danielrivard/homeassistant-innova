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
from homeassistant.const import ATTR_TEMPERATURE, PRECISION_WHOLE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from innova_controls import Mode

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
    async_add_entities([InnovaEntity(coordinator)])


class InnovaEntity(CoordinatorEntity, ClimateEntity):
    """Representation of an Innova AC Unit controls."""

    def __init__(self, coordinator: InnovaCoordinator):
        """Initialize the thermostat."""
        self._innova = coordinator.innova
        self._device_info = InnovaDeviceInfo(self._innova)

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.SWING_MODE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.PRESET_MODE
        )

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
        return self._innova.serial

    @property
    def precision(self):
        """Return the precision of the system."""
        return PRECISION_WHOLE

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self) -> float:
        """Return the current temperature."""
        return self._innova.ambient_temp

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._innova.target_temperature

    @property
    def target_temperature_step(self) -> float | None:
        """Return the temperature step by which it can be increased/decreased."""
        return 1.0

    @property
    def min_temp(self) -> float:
        return self._innova.min_temperature

    @property
    def max_temp(self) -> float:
        return self._innova.max_temperature

    @property
    def hvac_action(self):
        """Return the current state of the thermostat."""
        if not self._innova.power:
            return HVACAction.OFF

        mode = self._innova.mode
        if mode == Mode.HEATING:
            return HVACAction.HEATING
        if mode == Mode.COOLING:
            return HVACAction.COOLING
        if mode == Mode.DEHUMIDIFICATION:
            return HVACAction.DRYING
        if mode == Mode.FAN_ONLY:
            return HVACAction.FAN
        if mode == Mode.AUTO:
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
        if not self._innova.power:
            return HVACMode.OFF

        if self._innova.mode == Mode.COOLING:
            return HVACMode.COOL
        if self._innova.mode == Mode.HEATING:
            return HVACMode.HEAT
        if self._innova.mode == Mode.DEHUMIDIFICATION:
            return HVACMode.DRY
        if self._innova.mode == Mode.FAN_ONLY:
            return HVACMode.FAN_ONLY
        if self._innova.mode == Mode.AUTO:
            return HVACMode.AUTO
        return HVACMode.OFF

    @property
    def hvac_modes(self):
        """Return available HVAC modes."""
        return [
            HVACMode.OFF,
            HVACMode.COOL,
            HVACMode.HEAT,
            HVACMode.DRY,
            HVACMode.FAN_ONLY,
            HVACMode.AUTO,
        ]

    @property
    def preset_modes(self) -> list[str] | None:
        return [PRESET_NONE, PRESET_SLEEP]

    @property
    def preset_mode(self) -> str | None:
        if self._innova.night_mode == True:
            return PRESET_SLEEP
        if self._innova.night_mode == False:
            return PRESET_NONE
        return None

    @property
    def fan_modes(self) -> list[str] | None:
        return [FAN_AUTO, FAN_LOW, FAN_MEDIUM, FAN_HIGH]

    @property
    def fan_mode(self) -> str | None:
        if self._innova.fan_speed == 0:
            return FAN_AUTO
        if self._innova.fan_speed == 1:
            return FAN_LOW
        if self._innova.fan_speed == 2:
            return FAN_MEDIUM
        if self._innova.fan_speed == 3:
            return FAN_HIGH
        return None

    @property
    def swing_modes(self) -> list[str] | None:
        return [SWING_OFF, SWING_ON]

    @property
    def swing_mode(self) -> str | None:
        if self._innova.rotation:
            return SWING_ON
        else:
            return SWING_OFF

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        if hvac_mode == HVACMode.OFF:
            await self._innova.power_off()
        if hvac_mode == HVACMode.COOL:
            await self._innova.set_mode(Mode.COOLING)
        if hvac_mode == HVACMode.HEAT:
            await self._innova.set_mode(Mode.HEATING)
        if hvac_mode == HVACMode.DRY:
            await self._innova.set_mode(Mode.DEHUMIDIFICATION)
        if hvac_mode == HVACMode.FAN_ONLY:
            await self._innova.set_mode(Mode.FAN_ONLY)
        if hvac_mode == HVACMode.AUTO:
            await self._innova.set_mode(Mode.AUTO)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if preset_mode == PRESET_SLEEP:
            await self._innova.night_mode_on()
        if preset_mode == PRESET_NONE:
            await self._innova.night_mode_off()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        if fan_mode == FAN_AUTO:
            await self._innova.set_fan_speed(0)
        if fan_mode == FAN_LOW:
            await self._innova.set_fan_speed(1)
        if fan_mode == FAN_MEDIUM:
            await self._innova.set_fan_speed(2)
        if fan_mode == FAN_HIGH:
            await self._innova.set_fan_speed(3)

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        if swing_mode == SWING_ON:
            await self._innova.rotation_on()
        if swing_mode == SWING_OFF:
            await self._innova.rotation_off()

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        await self._innova.set_temperature(temperature)
