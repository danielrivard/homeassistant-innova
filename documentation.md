Hi, I have found that the Innova actually has a local REST API easily available through port 80, I reversed engineered it a bit and found most of the commands (that I actually use) to operate it. I'd like to write an integration for it, but haven't gone through all the HA documentation to understand how to achieve that.

Not sure yet how I could integrate with home assistant. There is maybe the RESTful integration that could work. Otherwise I am thinking of writing an actual climate integration in python.

I can't promise anything though.

Here's the information I was able to gather.

When data is expected for a command, it has to be form encoded (Content-Type: application/x-www-form-urlencoded).

|Action|URL|Data Needed|Extra Info|
|---|---|---|---|
|Status|GET http://[IP_ADDRESS]/api/v/1/status||Returns json object|
|Power ON|POST http://[IP_ADDRESS]/api/v/1/power/on|||
|Power OFF|POST http://[IP_ADDRESS]/api/v/1/power/off|||
|Set point|POST http://[IP_ADDRESS]/api/v/1/set/setpoint|p_temp=24||
|Rotation ON|POST http://[IP_ADDRESS]/api/v/1/set/feature/rotation|value=0||
|Rotation OFF|POST http://[IP_ADDRESS]/api/v/1/set/feature/rotation|value=7||
|Fan Speed|POST http://[IP_ADDRESS]/api/v/1/set/fan|value=[0-3]|0=auto  + 1,2,3|
|Dehumidification|POST http://[IP_ADDRESS]/api/v/1/set/mode/dehumidification|||
|Fan Only|POST http://[IP_ADDRESS]/api/v/1/set/mode/fanonly|||
|Cooling|POST http://[IP_ADDRESS]/api/v/1/set/mode/cooling|||
|Auto|POST http://[IP_ADDRESS]/api/v/1/set/mode/auto|||

JSON returned by status endpoint:
```
{
    "RESULT": {
        "a": [],
        "cci": 0,
        "ccv": 0,
        "cfg_lastWorkingMode": 4,
        "cloudConfig": 1,
        "cloudStatus": 4,
        "cm": 0,
        "connectionStatus": 2,
        "coolingDisabled": 0,
        "cp": 0,
        "daynumber": 0,
        "fr": 7,                       <--- Fan Rotation: 0=on 7=off
        "fs": 0,                       <--- Fan Speed: 0=auto, 1, 2, 3
        "heap": 11760,
        "heatingDisabled": 1,
        "heatingResistance": 0,
        "hotelMode": 0,
        "inputFlags": 0,
        "kl": 0,
        "lastRefresh": 3956,
        "ncc": 0,
        "nm": 0,
        "ns": 0,
        "ps": 0,                        <--- Power: 0=off, 1=on
        "pwd": "************",
        "sp": 26,                       <--- Temperature Set point
        "t": 16,                        <--- Ambient Temperature
        "timerStatus": 0,
        "uptime": 159660,
        "uscm": 0,
        "wm": 4                         <--- Mode: 1=cooling, 3=dehumidification, 4=fanonly. 5=auto
    },
    "UID": "[MAC ADDRESS]",
    "deviceType": "001",
    "net": {
        "dhcp": "1",
        "gw": "XXX.XXX.XXX.XXX",
        "ip": "XXX.XXX.XXX.XXX",
        "sub": "255.255.255.0"
    },
    "setup": {
        "name": "Device Name",
        "serial": "YYYYYYYYY"
    },
    "success": true,
    "sw": {
        "V": "1.0.42"
    },
    "time": {
        "d": 5,
        "h": 17,
        "i": 40,
        "m": 2,
        "y": 2022
    }
}

```