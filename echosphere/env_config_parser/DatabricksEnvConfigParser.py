from configparser import ConfigParser


class DatabricksAgentConfig:
    """Load Databricks connection settings from es.ini for the selected environment."""

    def __init__(self, env_name: str | None = None) -> None:
        """
        Initialize configuration using the given env section or default.

        :param env_name: Environment section name; if None, use [default].env.
        """
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
