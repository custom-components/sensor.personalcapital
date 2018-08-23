"""
Support for Personal Capital sensors.

For more details about this platform, please refer to the documentation at
https://github.com/custom-components/sensor.personalcapital
"""

import logging
import voluptuous as vol
import json
from datetime import timedelta
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)

__version__ = '0.0.1'

REQUIREMENTS = ['personalcapital==1.0.1']

CONF_EMAIL = 'email'
CONF_PASSWORD = 'password'
CONF_UNIT_OF_MEASUREMENT = 'unit_of_measurement'

DATA_PERSONAL_CAPITAL = 'personalcapital_cache'
DATA = 'personalcapital_data'
ATTR_NETWORTH = 'networth'

SCAN_INTERVAL = timedelta(seconds=500)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT, default='USD'): cv.string,
})

_CONFIGURING = {}
_LOGGER = logging.getLogger(__name__)

def request_app_setup(hass, config, pc, add_devices, discovery_info=None):
    """Request configuration steps from the user."""
    from personalcapital import PersonalCapital, RequireTwoFactorException, TwoFactorVerificationModeEnum
    configurator = hass.components.configurator

    def personalcapital_configuration_callback(data):
        """Run when the configuration callback is called."""
        from personalcapital import PersonalCapital, RequireTwoFactorException, TwoFactorVerificationModeEnum

        pc.two_factor_authenticate(TwoFactorVerificationModeEnum.SMS, data.get('verification_code'))
        result = pc.authenticate_password(config.get(CONF_PASSWORD))
        # result = 0

        if result == RequireTwoFactorException:
            configurator.notify_errors(_CONFIGURING['personalcapital'], "Invalid verification code")
        else:
            continue_setup_platform(hass, config, pc, add_devices, discovery_info)

    if 'personalcapital' not in _CONFIGURING:
        try:
            pc.login(config.get(CONF_EMAIL), config.get(CONF_PASSWORD))
        except RequireTwoFactorException:
            pc.two_factor_challenge(TwoFactorVerificationModeEnum.SMS)

    _CONFIGURING['personalcapital'] = configurator.request_config(
        'Personal Capital',
        personalcapital_configuration_callback,
        description="Please check text and enter the verification code below",
        submit_caption='Verify',
        fields=[{
            'id': 'verification_code',
            'name': "Verification code",
            'type': 'string'}]
    )

def setup_platform(hass, config, pc, add_devices, discovery_info=None):
    """Set up the Personal Capital component."""
    from personalcapital import PersonalCapital, RequireTwoFactorException, TwoFactorVerificationModeEnum
    pc = PersonalCapital()
    request_app_setup(hass, config, pc, add_devices, discovery_info)

def continue_setup_platform(hass, config, pc, add_devices, discovery_info=None):
    """Set up the Personal Capital component."""
    if "personalcapital" in _CONFIGURING:
        hass.components.configurator.request_done(_CONFIGURING.pop("personalcapital"))
        uom = config.get(CONF_UNIT_OF_MEASUREMENT)
        add_devices([PersonalCapitalNetWorthSensor(pc, uom)])

class PersonalCapitalNetWorthSensor(Entity):
    """Representation of a personalcapital.com net worth sensor."""

    def __init__(self, pc, unit_of_measurement):
        """Initialize the sensor."""
        self._pc = pc
        self._unit_of_measurement = unit_of_measurement
        self._state = None
        self._networth = None
        self.update()

    def update(self):
        """Get the latest state of the sensor."""
        result = self._pc.fetch('/newaccount/getAccounts')
        _LOGGER.warn('/newaccount/getAccounts')

        if not result:
            return False

        spData = result.json()['spData']
        networth = spData.get('networth', 0.0)
        _LOGGER.warn(networth)
        self._state = networth
        self._networth = networth


        # self._assets = self._personal_capital_data.assets
        # self._liabilities = self._personal_capital_data.liabilities
        # self._investments = self._personal_capital_data.investmentAccountsTotal
        # self._mortgages = self._personal_capital_data.mortgageAccountsTotal
        # self._cash = self._personal_capital_data.cashAccountsTotal
        # self._otherAssets =self._personal_capital_data.otherAssetAccountsTotal
        # self._otherLiabilities = self._personal_capital_data.otherLiabilitiesAccountsTotal
        # self._creditCards = self._personal_capital_data.creditCardAccountsTotal
        # self._loans = self._personal_capital_data.loanAccountsTotal

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Personal Capital Networth'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measure this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return 'mdi:coin'

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return {
            ATTR_NETWORTH: self._networth,
        }

# class AccountSensor(Entity):
#     """Representation of a personalcapital.com sensor."""

#     def __init__(self, personal_capital_data, name, currency):
#         """Initialize the sensor."""
#         self._personal_capital_data = personal_capital_data
#         self._name = "Personal Capital {}".format(name)
#         self._state = None
#         self._acct_type = None
#         self._category = None
#         self._firm_name = None
#         self._unit_of_measurement = currency

#     @property
#     def name(self):
#         """Return the name of the sensor."""
#         return self._name

#     @property
#     def state(self):
#         """Return the state of the sensor."""
#         return self._state

#     @property
#     def unit_of_measurement(self):
#         """Return the unit of measurement this sensor expresses itself in."""
#         return self._unit_of_measurement

#     @property
#     def icon(self):
#         """Return the icon to use in the frontend."""
#         return ACCOUNT_ICON

#     @property
#     def device_state_attributes(self):
#         """Return the state attributes of the sensor."""
#         return {
#             ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
#             ATTR_FIRM_NAME: self._firm_name,
#             ATTR_ACCT_TYPE: self._acct_type,
#             ATTR_CATEGORY: self._category
#         }

#     def update(self):
#         """Get the latest state of the sensor."""
#         self._personal_capital_data.update()
#         for account in self._personal_capital_data:
#             if self._name == "Personal Capital {}".format(account['name']):
#                 self._state = account['balance']
#                 self._firm_name = account['firmName']
#                 self._acct_type = account['accountType']
#                 self._category = account['productType']
#                 self._unit_of_measurement = account['currency']
