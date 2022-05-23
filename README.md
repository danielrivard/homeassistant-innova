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

### Configuration

#### From UI
This integration can be configured from the HA UI. You may need a hard refresh in your browser if you just installed the component.

##### Go to Settings -> Devices & Services

<img src="https://user-images.githubusercontent.com/2893453/169904177-26647057-da76-4aea-b69b-54ffc736fe0c.png" width="400"/>

##### Then Add Integrations
<img src="https://user-images.githubusercontent.com/2893453/169904299-b64b0d2b-889c-4efe-b9de-46f64d0fe210.png" width="300"/>

##### Search for Innova
![image](https://user-images.githubusercontent.com/2893453/169904659-202e9d07-19ca-4b98-a30c-d83678394221.png)

##### Configure the IP Address and optionally the area 
![image](https://user-images.githubusercontent.com/2893453/169904756-59319900-ce0c-41ec-8fdd-66861758b090.png)
![image](https://user-images.githubusercontent.com/2893453/169904861-43500d8f-3365-459c-b9e7-f3fd7efe5bd9.png)
##### That's it, you now have an Innova device and entity configured
![image](https://user-images.githubusercontent.com/2893453/169904968-11df645f-d3c1-4000-9219-6fd9ac8d68e8.png)

<img src="https://user-images.githubusercontent.com/2893453/169905005-c2ada883-ca09-440e-9cc4-7e5a9630cb64.png" width="500"/>

##### Repeat the process for multiple units

#### Yaml
* Next, in HA's configuration.yaml you would need to add this new integration
  * ``` yaml
    climate:
      - platform: innova
        host: [IP_ADDRESS_OF_INNOVA_UNIT]
        scan_interval: 1200
      - platform: innova
        host: [IP_ADDRESS_OF_OTHER_UNIT]
        scan_interval: 1200
    ```
  * Where host being the IP address of your innova unit (Strongly suggested that you give it a reserved DHCP address in your router, so it never changes)
  * scan_interval is how often HA will contact the unit to retrieve its state (300s => 5 minutes)
    * I found that scanning too often leads to the unit stopping to respond.
    * When a setting is changed, and the command receives a successful response, it will update the internal state of HA without needing to wait for a scan
  * Restart Home Assistant


At this point you should have a new entity that can control the Innova unit.
