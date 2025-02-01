from configparser import ConfigParser


class SnowflakeAgentConfig:
    def __init__(self, agent_name: str = None):
        config = ConfigParser()
        config.read('es.ini')
        if not agent_name:
            default_agent = config.get("default", "agent")
        else:
            default_agent = agent_name

        self.user = config.get(default_agent, "user")
        self.password = config.get(default_agent, "password")
        self.account = config.get(default_agent, "account")
        self.warehouse = config.get(default_agent, "warehouse")
        self.role = config.get(default_agent, "role")
        self.database = config.get(default_agent, "database")
        self.schema = config.get(default_agent, "schema")
