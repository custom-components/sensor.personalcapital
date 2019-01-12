[![Version](https://img.shields.io/badge/version-0.0.8-green.svg?style=for-the-badge)](#) [![mantained](https://img.shields.io/maintenance/yes/2019.svg?style=for-the-badge)](#)

[![maintainer](https://img.shields.io/badge/maintainer-Ian%20Richardson%20%40iantrich-blue.svg?style=for-the-badge)](#)

## Support
Hey dude! Help me out for a couple of :beers: or a :coffee:!

[![coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/zJtVxUAgH)

# sensor.personalcapital
Personal Capital component for [Home Assistant](https://www.home-assistant.io/)

To get started put `/custom_components/sensor/personalcapital.py` here:
`<config directory>/custom_components/sensor/personalcapital.py`. You can use this component with the custom [Personal Capital Lovelace card](https://github.com/custom-cards/pc-card). 

**Example configuration.yaml:**

```yaml
sensor:
  platform: personalcapital
  email: iantrich@email.com
  password: 12345
  unit_of_measurement: CAD
  monitored_categories:
    - assets
    - investments
```

**Configuration variables:**

key | description
:--- | :---
**platform (Required)** | `personalcapital``
**email (Required)** | Email for personalcapital.com
**password (Required)** | Password for personalcapital.com
**unit_of_measurement (Optional)** | Unit of measurement for your accounts **Default** USD
**monitored_categories (Optional)** | Banking categories to monitor. By default all categories are monitored. Options are `networth, assets, liabilities, investments, mortgages, cash, other_assets, other_liabilities, credit_cards, loans` 
***

**Note: You'll get a text message with your pin code to use on the frontend to configure**

Due to how `custom_components` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.
