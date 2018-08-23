# sensor.personalcapital
RSS feed custom component for Home Assistant

To get started put `/custom_components/sensor/personalcapital.py` here:
`<config directory>/custom_components/sensor/personalcapital.py`

**Example configuration.yaml:**

```yaml
sensor:
  platform: personalcapital
  email: iantrich@email.com
  password: 12345
  unit_of_measurement: CAD
```

**Configuration variables:**

key | description
:--- | :---
**platform (Required)** | `personalcapital``
**email (Required)** | Email for personalcapital.com
**password (Required)** | Password for personalcapital.com
**unit_of_measurement (Optional)** | Unit of measurement for your accounts **Default** USD

***

**Note: You'll get a text message with your pin code to use on the frontend to configure**

Due to how `custom_components` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.