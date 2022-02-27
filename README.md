# homeassistant-innova

Custom Component for controlling an Innova 2.0 Heat Pump in Home Assistant

## Installation

In its current state, it can be installed as a custom component in Home Assistant. I need to make it compliant with Home Assistant's standards and submit it for inclusion in the core.

To manually install, follow these steps:

* In Home Assistant's config directory, you need to create a custom_components and an innova folder under it.
  * config/custom_components/innova
* In this directory, you need to put these:
  * \_\_init\_\_.py
  * climate.py
  * manifest.json
* Next, in HA's configuration.yaml you would need to add this new integration
  * ``` yaml
    climate:
      - platform: innova
        host: [IP_ADDRESS_OF_INNOVA_UNIT]
        scan_interval: 300
    ```
  * Where host being the IP address of your innova unit (Strongly suggested that you give it a reserved DHCP address in your router, so it never changes)
  * scan_interval is how often HA will contact the unit to retrieve its state (300s => 5 minutes)
    * I found that scanning too often leads to the unit stopping to respond.
    * When a setting is changed, and the command receives a successful response, it will update the internal state of HA without needing to wait for a scan
  * Restart Home Assistant


At this point you should have a new entity that can control the Innova unit.
