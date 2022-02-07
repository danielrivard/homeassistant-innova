import json
from enum import Enum

import requests

CMD_STATUS = "status"

CMD_POWER_ON = "power/on"
CMD_POWER_OFF = "power/off"

CMD_SET_TEMP = "set/setpoint"

CMD_ROTATION = "set/feature/rotation"
ROTATION_ON = 0
ROTATION_OFF = 7

CMD_FAN_SPEED = "set/fan"

MIN_TEMP = 16
MAX_TEMP = 31


class Mode(Enum):
    COOLING = {"cmd": "set/mode/cooling", "code": 1, "status": "cooling"}
    HEATING = {"cmd": "set/mode/heating", "code": 2, "status": "heating"}
    DEHUMIDIFICATION = {
        "cmd": "set/mode/dehumidification",
        "code": 3,
        "status": "dehumidification",
    }
    FAN_ONLY = {"cmd": "set/mode/fanonly", "code": 4, "status": "fanonly"}
    AUTO = {"cmd": "set/mode/auto", "code": 5, "status": "auto"}
    UNKNOWN = {}


class Innova:
    def __init__(self, host):
        self._api_url = f"http://{host}/api/v/1"
        self._data = {}
        self._status = {}

    def update(self):
        status_url = f"{self._api_url}/{CMD_STATUS}"
        r = requests.get(status_url)
        data = json.loads(r.text)
        self._data = data
        if "RESULT" in data:
            self._status = data["RESULT"]

    @property
    def ambient_temp(self) -> int:
        if "t" in self._status:
            return self._status["t"]
        else:
            return 0

    @property
    def target_temperature(self) -> int:
        if "sp" in self._status:
            return self._status["sp"]
        else:
            return 0

    @property
    def min_temperature(self) -> int:
        return MIN_TEMP

    @property
    def max_temperature(self) -> int:
        return MAX_TEMP

    @property
    def power(self) -> bool:
        if "ps" in self._status:
            return self._status["ps"] == 1
        return False

    @property
    def mode(self) -> Mode:
        if "wm" in self._status:
            for mode in Mode:
                if self._status["wm"] == mode.value["code"]:
                    return mode
        return Mode.UNKNOWN

    @property
    def rotation(self) -> bool:
        if "fr" in self._status:
            if self._status["fr"] == ROTATION_ON:
                return True
        return False

    @property
    def fan_speed(self) -> int:
        if "fs" in self._status:
            return self._status["fs"]
        return 0

    @property
    def name(self) -> str:
        if "setup" in self._data and "name" in self._data["setup"]:
            return self._data["setup"]["name"]
        return None

    @property
    def id(self) -> str:
        if "setup" in self._data and "serial" in self._data["setup"]:
            return self._data["setup"]["serial"]
        return None

    def send_command(self, command, data=None) -> bool:
        cmd_url = f"{self._api_url}/{command}"
        if data:
            r = requests.post(cmd_url, data=data)
        else:
            r = requests.post(cmd_url)
        if r.status_code == 200:
            result = json.loads(r.text)
            if result["success"]:
                return True
        return False

    def power_on(self):
        if self.send_command(CMD_POWER_ON):
            self._status["ps"] = 1

    def power_off(self):
        if self.send_command(CMD_POWER_OFF):
            self._status["ps"] = 0

    def rotation_on(self):
        if self.send_command(CMD_ROTATION, {"value": ROTATION_ON}):
            self._status["fr"] = ROTATION_ON

    def rotation_off(self):
        if self.send_command(CMD_ROTATION, {"value": ROTATION_OFF}):
            self._status["fr"] = ROTATION_OFF

    def set_temperature(self, temperature: int):
        data = {"p_temp": temperature}
        if self.send_command(CMD_SET_TEMP, data):
            self._status["sp"] = temperature

    def set_fan_speed(self, speed: int):
        data = {"value": speed}
        if self.send_command(CMD_FAN_SPEED, data):
            self._status["fs"] = speed

    def set_mode(self, mode: Mode):
        if self.send_command(mode.value["cmd"]):
            self._status["wm"] = mode.value["code"]
