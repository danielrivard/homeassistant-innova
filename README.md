[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# homeassistant-innova

Custom Component for controlling an Innova 2.0 Heat Pump in Home Assistant

## Installation

### HACS Custom Repository

The Innova integration can be installed as an HACS custom repository.

Follow these [instructions](https://hacs.xyz/docs/faq/custom_repositories) from HACS.

There is also a tutorial [here](https://codingcyclist.medium.com/how-to-install-any-custom-component-from-github-in-less-than-5-minutes-ad84e6dc56ff)

### Manual Installation

You can also manually install as a custom component on your Home Assistant installation.

Follow these steps:

* In Home Assistant's config directory, you need to create a custom_components and an innova folder under it.
  * config/custom_components/innova
* In this directory, you need to copy these files from this repository:
  * [\_\_init\_\_.py](custom_components/innova/__init__.py)
  * [climate.py](custom_components/innova/climate.py)
  * [manifest.json](custom_components/innova/manifest.json)
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
