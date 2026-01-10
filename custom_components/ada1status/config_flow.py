"""Config flow for Ada1Status integration."""
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    host = data[CONF_HOST]
    
    # Ensure URL format
    if not host.startswith(("http://", "https://")):
        host = f"http://{host}"
    
    session = async_get_clientsession(hass)
    
    try:
        async with session.get(host, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status != 200:
                raise ConnectionError(f"HTTP {response.status}")
            # Try to read some data to verify it's accessible
            await response.text()
    except aiohttp.ClientError as err:
        raise ConnectionError(f"Cannot connect to {host}: {err}") from err
    except Exception as err:
        raise ConnectionError(f"Unknown error: {err}") from err

    return {"title": DEFAULT_NAME, "host": host}


class Ada1StatusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ada1Status."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                }
            ),
            errors=errors,
        )
