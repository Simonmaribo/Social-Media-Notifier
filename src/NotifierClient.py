from .platforms import YoutubeClient


class NotifierClient:
    def __init__(self):
        self.platforms = {}

    def get_platform(self, platform: str):
        if not (platform.lower() in self.platforms):
            raise KeyError(f"Platform '{platform.lower()}' not registered in client.")
        return self.platforms[platform.lower()]

    def register_platform(self, platform: str, api_key: str = None, timer: int = 30):
        if api_key is None:
            raise TypeError(f"api_key was none - please insert an api key")
        elif platform.lower() in self.platforms:
            raise KeyError(f"Platform '{platform.lower()}' has already been registered.")
        switcher = {
            "youtube": YoutubeClient
        }
        if not (platform.lower() in switcher):
            raise KeyError(f"Platform does not exist, please use one of the following: {switcher.keys()}")
        self.platforms[platform.lower()] = switcher.get(platform.lower())(api_key, timer)
        return self.get_platform(platform)

    def get_platforms(self):
        """ Returns a List[PlatformBase] with all registered platforms."""
        return self.platforms.values()
