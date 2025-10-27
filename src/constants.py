from enum import Enum


class Environment(str, Enum):
    LOCAL = "LOCAL"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self == self.LOCAL

    @property
    def is_deployed(self) -> bool:
        return self == self.PRODUCTION