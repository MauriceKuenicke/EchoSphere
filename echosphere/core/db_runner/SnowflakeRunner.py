import time

import snowflake.connector
from snowflake.connector import ProgrammingError

from echosphere.env_config_parser.SnowflakeEnvConfigParser import SnowflakeAgentConfig


class SnowflakeRunner:
    """
    A utility class for executing SQL tests against a Snowflake database.
    """

    @classmethod
    def dispatch_test(cls, env: str | None, test_file_path: str) -> tuple[int, float, str]:
        """
        Execute a SQL test against Snowflake and return results.

        :param env: Name of the environment/agent to use from es.ini.
        :param test_file_path: Path to the SQL test file to execute.
        :return: A tuple of (row_count, execution_time_seconds, sql_text).
        """
        sf_agent = SnowflakeAgentConfig(agent_name=env)
        with snowflake.connector.connect(
            user=sf_agent.user,
            password=sf_agent.password,
            account=sf_agent.account,
            warehouse=sf_agent.warehouse,
            role=sf_agent.role,
            database=sf_agent.database,
            schema=sf_agent.schema,
            session_parameters={
                "QUERY_TAG": "EchoSphere Testing Suite Run",
            },
            application="EchoSphere",
        ) as conn:
            cur = conn.cursor()
            with open(test_file_path, "r") as s:
                sql = s.read()

            start_time = time.time()
            cur.execute_async(sql)

            try:
                qry_id = cur.sfqid
                if not qry_id:
                    raise Exception("No query ID returned from Snowflake.")
                while conn.is_still_running(conn.get_query_status(qry_id)):
                    time.sleep(2)
            except ProgrammingError as err:
                raise Exception("Programming Error: {0}".format(err))

            end_time = time.time()
            execution_time = round(end_time - start_time, 3)
            cur.query_result(qry_id)
            row_count = cur.rowcount
            if not row_count:
                raise Exception("No row count returned from Snowflake.")

        return row_count, execution_time, sql
