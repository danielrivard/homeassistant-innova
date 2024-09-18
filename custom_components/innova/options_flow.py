from homeassistant import config_entries
import voluptuous as vol
from datetime import timedelta

from .const import DOMAIN


class InnovaOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize the Innova options flow handler."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options for the Innova integration."""
        if user_input is not None:
            # Store the update interval in seconds in Home Assistant's data
            self.hass.data["innova_update_interval_seconds"] = user_input["update_interval_seconds"]
            return self.async_create_entry(title="", data=user_input)

        # Default to 300 seconds (5 minutes) if not set
        current_interval = self.config_entry.options.get("update_interval_seconds", 300)

        # Define the form schema for the update interval in seconds
        schema = vol.Schema(
            {
                vol.Required("update_interval_seconds", default=current_interval): vol.All(vol.Coerce(int), vol.Range(min=1)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
