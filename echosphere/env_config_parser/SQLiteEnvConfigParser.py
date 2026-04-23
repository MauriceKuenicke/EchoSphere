from configparser import ConfigParser


class SQLiteAgentConfig:
    """Load SQLite connection settings from es.ini for the selected environment."""

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

        if config.has_option(section, "database"):
            self.database: str = config.get(section, "database")
        else:
            raise Exception(f"Missing 'database' in section [{section}] of es.ini")
