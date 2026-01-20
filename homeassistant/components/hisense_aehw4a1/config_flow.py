"""Config flow for Hisense AEH-W4A1."""

from __future__ import annotations

import ipaddress
import logging
from typing import Any

from pyaehw4a1.aehw4a1 import AehW4a1
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class HisenseConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hisense AEH-W4A1."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the user step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()

            try:
                ipaddress.IPv4Address(host)
            except ipaddress.AddressValueError:
                errors[CONF_HOST] = "invalid_host"
            else:
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()

                try:
                    await AehW4a1(host).check()
                except Exception:
                    _LOGGER.exception("Cannot connect to %s", host)
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(
                        title=f"Hisense AC ({host})",
                        data={CONF_HOST: host},
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
            }),
            errors=errors,
        )
