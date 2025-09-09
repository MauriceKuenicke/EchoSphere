from configparser import ConfigParser
from typing import Optional


class DatabricksAgentConfig:
    """
    Load Databricks agent configuration from `es.ini`.

    This class reads the `es.ini` file and extracts the connection parameters for a
    selected environment section. If no env name is provided, it uses the `[default]`
    section's `env` key to resolve the active environment.

    Required keys in the target section:
      - server_hostname
      - http_path
      - access_token

    Optional keys:
      - catalog
      - schema
    """

    def __init__(self, env_name: Optional[str] = None) -> None:
        config = ConfigParser()
        config.read("es.ini")
        section = config.get("default", "env") if not env_name else env_name
        if not config.has_section(section):
            raise Exception(f"Environment section '{section}' not found in es.ini")

        required = ["server_hostname", "http_path", "access_token"]
        missing = [k for k in required if not config.has_option(section, k)]
        if missing:
            raise Exception(
                f"Missing required option(s) {missing} in section [{section}] of es.ini for Databricks configuration"
            )

        self.server_hostname: str = config.get(section, "server_hostname")
        self.http_path: str = config.get(section, "http_path")
        self.access_token: str = config.get(section, "access_token")

        # Optional
        self.catalog: str | None = config.get(section, "catalog", fallback=None)
        self.schema: str | None = config.get(section, "schema", fallback=None)
