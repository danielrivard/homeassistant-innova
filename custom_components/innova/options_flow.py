"""Options flow for the Innova integration."""
from homeassistant import config_entries
import voluptuous as vol
from .const import DEFAULT_SCAN_INTERVAL

class InnovaOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Innova integration."""

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "scan_interval", 
                    default=options.get("scan_interval", DEFAULT_SCAN_INTERVAL)
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=86400)),
            })
        )
