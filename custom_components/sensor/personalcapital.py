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
ATTR_ASSETS = 'assets'
ATTR_LIABILITIES = 'liabilities'
ATTR_INVESTMENTS = 'investments'
ATTR_MORTGAGES = 'mortgages'
ATTR_CASH = 'cash'
ATTR_OTHER_ASSETS = 'other_assets'
ATTR_OTHER_LIABILITIES = 'other_liabilities'
ATTR_CREDIT_CARDS = 'credit_cards'
ATTR_LOANS = 'loans'

SCAN_INTERVAL = timedelta(hours=1)

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
        description="Verification code sent to phone",
        submit_caption='Verify',
        fields=[{
            'id': 'verification_code',
            'name': "Verification code",
            'type': 'string'}]
    )

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Personal Capital component."""
    from personalcapital import PersonalCapital, RequireTwoFactorException, TwoFactorVerificationModeEnum
    pc = PersonalCapital()
    request_app_setup(hass, config, pc, add_devices, discovery_info)

def continue_setup_platform(hass, config, pc, add_devices, discovery_info=None):
    """Set up the Personal Capital component."""
    if "personalcapital" in _CONFIGURING:
        hass.components.configurator.request_done(_CONFIGURING.pop("personalcapital"))
        uom = config.get(CONF_UNIT_OF_MEASUREMENT)
        add_devices([PersonalCapitalNetWorthSensor(pc, uom)], True)

class PersonalCapitalNetWorthSensor(Entity):
    """Representation of a personalcapital.com net worth sensor."""

    def __init__(self, pc, unit_of_measurement):
        """Initialize the sensor."""
        self._pc = pc
        self._unit_of_measurement = unit_of_measurement
        self._state = None
        self._networth = None
        self._assets = None
        self._liabilities = None
        self._investments = None
        self._mortgages = None
        self._cash = None
        self._other_assets = None
        self._other_liabilities = None
        self._credit_cards = None
        self._loans = None
        self.update()

    def update(self):
        """Get the latest state of the sensor."""
        result = self._pc.fetch('/newaccount/getAccounts')

        if not result:
            return False

        spData = result.json()['spData']
        _LOGGER.warn(spData)
        self._state = spData.get('networth', 0.0)
        self._networth = spData.get('networth', 0.0)
        self._assets = spData.get('assets', 0.0)
        self._liabilities = spData.get('liabilities', 0.0)
        self._investments = spData.get('investmentAccountsTotal', 0.0)
        self._mortgages = spData.get('mortgageAccountsTotal', 0.0)
        self._cash = spData.get('cashAccountsTotal', 0.0)
        self._other_ssets = spData.get('otherAssetAccountsTotal', 0.0)
        self._other_iabilities = spData.get('otherLiabilitiesAccountsTotal', 0.0)
        self._credit_cards = spData.get('creditCardAccountsTotal', 0.0)
        self._loans = spData.get('loanAccountsTotal', 0.0)

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
            ATTR_NETWORTH: self._networth,
            ATTR_ASSETS: self._assets,
            ATTR_LIABILITIES: self._liabilities,
            ATTR_INVESTMENTS: self._investments,
            ATTR_MORTGAGES: self._mortgages,
            ATTR_CASH: self._cash,
            ATTR_OTHER_ASSETS: self._other_assets,
            ATTR_OTHER_LIABILITIES: self._other_liabilities,
            ATTR_CREDIT_CARDS: self._credit_cards,
            ATTR_LOANS: self._loans,
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
