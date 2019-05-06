# sensor.personalcapital
Personal Capital component for [Home Assistant](https://www.home-assistant.io/)

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE.md)

![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

## Support
Hey dude! Help me out for a couple of :beers: or a :coffee:!

[![coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/zJtVxUAgH)

To get started put all contents of `/custom_components/personalcapital/` here:
`<config directory>/custom_components/personalcapital/`. You can use this component with the custom [Personal Capital Lovelace card](https://github.com/custom-cards/pc-card).

**Example configuration.yaml:**

```yaml
sensor:
  platform: personalcapital
  email: iantrich@email.com
  password: 12345
  unit_of_measurement: CAD
  monitored_categories:
    - investment
    - cash
```

**Configuration variables:**

key | description
:--- | :---
**platform (Required)** | `personalcapital``
**email (Required)** | Email for personalcapital.com
**password (Required)** | Password for personalcapital.com
**unit_of_measurement (Optional)** | Unit of measurement for your accounts **Default** USD
**monitored_categories (Optional)** | Banking categories to monitor. By default all categories are monitored. Options are `investment, mortgage, cash, other_asset, other_liability, credit, loan` 
***

**Note: You'll get a text message with your pin code to use on the frontend to configure**

Due to how `custom_components` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.

[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/sensor.personalcapital.svg?style=for-the-badge
[commits]: https://github.com/custom-components/sensor.personalcapital/commits/master
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/t/lovelace-personal-capital-component-card/91463
[license-shield]: https://img.shields.io/github/license/custom-components/sensor.personalcapital.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Ian%20Richardson%20%40iantrich-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/sensor.personalcapital.svg?style=for-the-badge
[releases]: https://github.com/custom-components/sensor.personalcapital/releases
