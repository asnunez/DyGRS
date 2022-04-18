from dataclasses import dataclass
from typing import Dict


def bool2str(b: bool) -> str:
    return "True" if b else "False"


@dataclass
class Camera:
    alias: str
    host: str
    active: bool

    def to_dict(self) -> Dict:
        camera_info = {
            "camera":
                {
                    "alias": self.alias,
                    "url": f"rtsp://{self.host}",
                    "active": bool2str(self.active)
                }
        }

        return camera_info
