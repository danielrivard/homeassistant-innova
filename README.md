[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

![image](https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=integration%20usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.innova.total)


# homeassistant-innova

Custom Component for controlling some Innova Heat and A/C products through [Home Assistant](https://www.home-assistant.io/) ([2.0](https://www.innovaenergie.com/prodotti/climatizzatore-senza-unita-esterna/2.0-verticale/) and [AirLeaf](https://www.innovaenergie.com/prodotti/fancoils/airleaf/) currently supported)

## Installation

### HACS

The Innova integration is available through [HACS](https://hacs.xyz/).

[Download](https://hacs.xyz/docs/setup/prerequisites) and [configure](https://hacs.xyz/docs/configuration/basic) HACS. 

https://peyanski.com/how-to-install-home-assistant-community-store-hacs/

Once installed and configured, you can search for the Innova in HACS' integration section.

From there, jump to the [configuration](#configuration) of this readme to continue setup your Innova device.

### Manual Installation

You can also manually install as a custom component on your Home Assistant installation.

Follow these steps:

* In Home Assistant's config directory, you need to create a custom_components and an innova folder under it.
  * config/custom_components/innova
* In this directory, you need to copy these files from this repository:
  * [translations](custom_components/innova/translations/)
  * [\_\_init\_\_.py](custom_components/innova/__init__.py)
  * [climate.py](custom_components/innova/climate.py)
  * [config_flow.py](custom_components/innova/config_flow.py)
  * [const.py](custom_components/innova/const.py)
  * [coordinator.py](custom_components/innova/coordinator.py)
  * [device_info.py](custom_components/innova/device_info.py)
  * [manifest.json](custom_components/innova/manifest.json)
  * [sensor.py](custom_components/innova/sensor.py)
  * [string.json](custom_components/innova/string.json)

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

##### Restart Home Assistant


At this point you should have a new device with a climate entity that can control the Innova unit and a sensor entity for the current ambient temperature.
