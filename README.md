<p align="center">
  <a href="https://mauricekuenicke.github.io/echosphere/"><img src="docs/assets/logo-color-cropped.svg" alt="EchoSphere Logo" width="60%"></a>
</p>

<p align="center">
    <em>Snowflake Database Testing and Data Quality Assesements</em>
</p>

---

**Source Code**: <a href="https://github.com/MauriceKuenicke/EchoSphere" target="_blank">https://github.com/MauriceKuenicke/EchoSphere</a>

---
<p align="center">
<em>Derived from the mythological nymph Echo — cursed to only repeat the words of others — this
name symbolizes the power of reflection and reverberation. In Greek mythology, Echo's 
voice lingered in caves and valleys, mirroring sounds across vast expanses.</em></p>

Run parallelized SQL-based tests on Snowflake Databases. Lightweight, scalable, and customizable for different environments.

---
# ⚠️ Important
This project is currently not safe for use in a production environment. Use at your own risk.



# Usage

<p align="center">
  <img src="docs/assets/example.PNG" alt="Example Output" width="60%">
</p>


## Installation
```sh
pip install git+https://github.com/MauriceKuenicke/EchoSphere
```

## Setup
Inside your virtual environment run:
```
es setup
```
This will set up a default location to store your SQL tests in as well as a configuration file for your Snowflake
credentials and environments.

EchoSphere test suites are just a collection of SQL files (i.e. `MY_TEST.es.sql`). 
The file ending `.es.sql` is important for EchoSphere to detect the test files. 
Each test needs to be written in a way that a successful execution will generate zero output rows.
As soon as a single row is returned, EchoSphere labels the test as failed.
SQL statements should not use full-path definitions for tables to allow for more flexibility when setting up
agents.

Example:
```sql
SELECT * FROM
    (SELECT
         SUM(O_TOTALPRICE) AS "SUM_TOTALPRICE"
     FROM ORDERS
     WHERE O_ORDERDATE = '1995-02-19')
WHERE "SUM_TOTALPRICE" <> 944870465.07;
```
This query will check that the sum of the total order prices for a past date matches an expected value.
If the values do not match, 
this query will return a single row containing the actual number calculated at runtime during the test.

## Environment Management
Different Snowflake environments (Agents) are managed in the `es.ini` file.

```
[default]
agent = agent.snowflake.dev  # Name of the agent that will be used if no command line argument is provided

[agent.snowflake.dev]
user = ...
password = ...
account = ...
warehouse = ...
role = ...
database = ...
schema = ...

[agent.snowflake.prod]
user = ...
password = ...
account = ...
warehouse = ...
role = ...
database = ...
schema = ...
```

When running tests, you can change the agent to be used by providing its name as an argument, like
```sh
es run -a agent.snowflake.dev
```

# Development
``
pip install -e .[dev]
``
