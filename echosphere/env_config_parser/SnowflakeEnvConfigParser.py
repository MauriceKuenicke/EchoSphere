from configparser import ConfigParser
from typing import Optional


class SnowflakeAgentConfig:
    """
    Load Snowflake agent configuration from `es.ini`.

    This class reads the `es.ini` file and extracts the credentials and
    connection parameters for a selected agent section. If no agent name is
    provided, it uses the `[default]` section's `agent` key to resolve the
    active agent.

    Attributes set on instances:
        user: Snowflake username.
        password: Snowflake password.
        account: Snowflake account identifier.
        warehouse: Default Snowflake warehouse.
        role: Snowflake role.
        database: Default database.
        schema: Default schema.

    :param agent_name: Optional explicit agent section name to use. If None,
                       the default agent is read from `[default].agent`.
    """

    def __init__(self, agent_name: Optional[str] = None) -> None:
        """
        Initialize the configuration by reading values from `es.ini`.

        :param agent_name: Optional agent section to read; if None, the
                           default agent is resolved from `[default].agent`.
        :return: None
        """
        config = ConfigParser()
        config.read("es.ini")
        if not agent_name:
            default_agent = config.get("default", "agent")
        else:
            default_agent = agent_name

        self.user: str = config.get(default_agent, "user")
        self.password: str = config.get(default_agent, "password")
        self.account: str = config.get(default_agent, "account")
        self.warehouse: str = config.get(default_agent, "warehouse")
        self.role: str = config.get(default_agent, "role")
        self.database: str = config.get(default_agent, "database")
        self.schema: str = config.get(default_agent, "schema")
