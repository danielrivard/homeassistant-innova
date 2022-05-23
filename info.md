## Usage:
#### Option 1: From UI
This integration can be configured through  the Home Assistant UI.

##### Go to Settings -> Devices & Services -> Add Integration

##### Search for Innova
![image](https://user-images.githubusercontent.com/2893453/169904659-202e9d07-19ca-4b98-a30c-d83678394221.png)

##### Configure the IP Address and optionally the area 
![image](https://user-images.githubusercontent.com/2893453/169904756-59319900-ce0c-41ec-8fdd-66861758b090.png)

#### Option 2: In configuration.yaml:

``` yaml
climate:
  - platform: innova
    host: [IP_ADDRESS_OF_INNOVA_UNIT]
    scan_interval: 900
  - platform: innova
    host: [IP_ADDRESS_OF_OTHER_INNOVA_UNIT]
    scan_interval: 900
```
