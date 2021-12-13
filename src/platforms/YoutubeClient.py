import asyncio
from datetime import datetime, timezone
import time

import requests

from ..base import PlatformBase


class YoutubeClient(PlatformBase):
    def __init__(self, api_key: str, timer: int = 30):
        super().__init__(platform="youtube", api_key=api_key, timer=timer)
        self.channels = {}

    # Internal Identifier
    # Youtube Channel ID to search for.
    def add_channel(self, identifier: str, channel_id: str):
        if identifier is None or channel_id is None:
            raise ValueError("identifier or channel_id was undefined")
        elif identifier in self.channels:
            raise KeyError(f"Identifier '{identifier}' already exists in channels. Remove it to add a new.")
        self.channels[identifier] = {"id": channel_id}

    def remove_channel(self, identifier: str):
        del self.channels[identifier]

    def get_channels(self):
        return self.channels

    def get_channel(self, identifier):
        return self.channels[identifier]

    async def _query(self):
        def is_newest_video(channel_identifier, identifier, published_at):
            # Check if the video is the same at the last saved video.
            if "lastSavedVideo" in self.get_channel(channel_identifier) and self.get_channel(channel_identifier)[
                "lastSavedVideo"] == identifier:
                return False
            publish_epochTime = time.mktime(time.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ"))
            # TODO: No work, rework this stuff
            if publish_epochTime < self._client_initialized_epoch_time:
                return False
            return True

        for channel in self.get_channels():
            try:
                playlist_id = "UU" + self.channels[channel]['id'][2:]
                response = requests.get(
                    f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&part=snippet&maxResults=5&key={self._get_api_key()}"
                    # f"https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={self.channels[channel]['id']}&key={self._get_api_key()}"
                )
                try:
                    resp = response.json()
                except ValueError:
                    print(f"Response for '{response.url}' had no json body.")
                    continue
                if response.status_code != 200 and "error" in resp:
                    raise Exception(resp["error"]["message"])
                elif response.status_code == 200:
                    if "items" in resp and len(resp["items"]) > 0:
                        item = resp["items"][0]["snippet"]
                        if not (item["resourceId"]["kind"] == "youtube#video"):
                            continue
                        if is_newest_video(channel, item["resourceId"]["videoId"], item["publishedAt"]):
                            self.channels[channel]["lastSavedVideo"] = item["resourceId"]["videoId"]
                            callback = self._get_callback()
                            callback(
                                {
                                    "platform": self._get_platform(),
                                    "type": "Video",
                                    "channelTitle": item["channelTitle"],
                                    "videoTitle": item["title"],
                                    "url": f"https://youtu.be/{item['resourceId']['videoId']}",
                                    "description": item["description"]
                                }
                            )
            except Exception as e:
                print(f"Exeception occurred: {e}")
                pass

    async def _create_timer(self):
        await asyncio.sleep(1)
        while True:
            await self._query()
            await asyncio.sleep(self._get_timer())

    def loop_in_thread(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._create_timer())

    def start(self):
        self._client_initialized_epoch_time = time.time()
        self._loop = asyncio.get_event_loop()
        self.loop_in_thread()
