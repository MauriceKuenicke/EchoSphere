from configparser import ConfigParser
from typing import Optional


class PlatformExtractor:
    """Utilities to read platform information from es.ini."""

    @classmethod
    def extract_platform_info(cls, env_name: Optional[str] = None) -> str:
        """Return the active platform name from es.ini in lower-case.

        :param env_name: Optional environment section to read; if None, uses `[default].env`.
        :return: The platform name (e.g., "snowflake").
        """
        config = ConfigParser()
        config.read("es.ini")

        if not env_name:
            default_env = config.get("default", "env")
        else:
            default_env = env_name

        return config.get(default_env, "platform").lower()