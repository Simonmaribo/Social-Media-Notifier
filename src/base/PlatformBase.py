class PlatformBase:
    def __init__(self, platform: str, api_key: str, timer: int = 30):
        self._settings = {
            "platform": platform,
            "api_key": api_key,
            "timer": timer,
        }

    def _get_api_key(self):
        if not("api_key" in self._settings):
            raise ValueError(f"api_key was undefined, expected string")
        return self._settings["api_key"]

    def _get_platform(self):
        if not("api_key" in self._settings):
            raise ValueError(f"platform was undefined, expected PlatformBase")
        return self._settings["platform"]

    def _get_callback(self):
        if not("callback" in self._settings):
            raise KeyError(f"No callback function defined for Platform: {self._get_platform()}")
        if self._settings["callback"] is None:
            raise ValueError(f"callback of Platform: {self._get_platform()} is None")
        return self._settings["callback"]

    def set_callback(self, func=None):
        if func is None:
            raise TypeError("set_callback requires 'func' parameter as a function to callback later.")
        self._settings["callback"] = func

    def _callback(self, payload):
        callback = self._get_callback()
        callback(payload)

    def _get_timer(self) -> int:
        if not("timer" in self._settings):
            raise ValueError(f"timer setting is undefined")
        return self._settings["timer"]