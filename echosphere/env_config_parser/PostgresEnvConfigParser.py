from configparser import ConfigParser


class PostgresAgentConfig:
    """
    Load PostgreSQL agent configuration from `es.ini`.

    This class reads the `es.ini` file and extracts the credentials and
    connection parameters for a selected environment section. If no env name is
    provided, it uses the `[default]` section's `env` key to resolve the
    active environment.

    :param env_name: Optional explicit environment section name to use. If None,
                       the default env is read from `[default].env`.
    """

    def __init__(self, env_name: str | None = None) -> None:
        """
        Initializes a configuration object using specified or default environment settings.

        This method reads environmental configurations from an INI file (es.ini) to retrieve
        details about the database connection and associated parameters. It validates that
        all required options ("host", "database") exist and assigns their respective values
        to instance attributes. Default and fallback options are used where applicable.

        :param env_name: The name of the environment whose configuration will be used. If not
            specified, it defaults to the "env" option within the "default" section of the
            configuration file.
        """
        config = ConfigParser()
        config.read("es.ini")
        section = config.get("default", "env") if not env_name else env_name
        if not config.has_section(section):
            raise Exception(f"Environment section '{section}' not found in es.ini")

        if config.has_option(section, "host"):
            self.host: str = config.get(section, "host")
        else:
            raise Exception(f"Missing 'host' in section [{section}] of es.ini")

        if config.has_option(section, "database"):
            self.database: str = config.get(section, "database")
        else:
            raise Exception(f"Missing 'database' in section [{section}] of es.ini")

        self.user: str = config.get(section, "user")
        self.password: str = config.get(section, "password")
        self.port: int = config.getint(section, "port", fallback=5432)
        self.schema: str | None = config.get(section, "schema", fallback=None)
        self.sslmode: str | None = config.get(section, "sslmode", fallback=None)
