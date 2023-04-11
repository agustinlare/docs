# pip3 install psycopg2 dbt-postgres
# python3 postgres_newdb.py $HOST $APP_NAME $ADMIN $PASSWORD
# Este script crea una nueva base de datos, un usuario para que pueda ser accedida desde el aplicativo
# cambia el ownership a dicho usuario para la herencia de permisos
import psycopg2, sys
import random, string, logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

if len(sys.argv) != 5:
  raise ValueError("Arguments missing. Should be \"python3 path/this.py $HOST $APP-NAME $ADMIN-USER $ADMIN-PASSWORD\"")

host = sys.argv[1]
app_database = sys.argv[2]
admin_user = sys.argv[3]
admin_pass = sys.argv[4]

def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

def create_conn(host, app, user, password):
  conn = psycopg2.connect(host=host, database=app, user=user, password=password)  
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  return conn.cursor()

def execute_querys(querys):
  for q in querys:
    cursor.execute(q)
    logging.info("Postgres runned: %s" % q)

# Create postgres connection
cursor = create_conn(host, "postgres", admin_user, admin_pass)

# Create database
cursor.execute("CREATE DATABASE %s" % app_database)
logging.info("Postgres %s database created" % app_database)

# Create app user
app_user = "%s_user" % app_database
app_password = get_random_string(8)
sql_create_user = "CREATE USER %s WITH ENCRYPTED PASSWORD '%s'" % (app_user, app_password)
cursor.execute(sql_create_user)
logging.info("Postgres %s user created with password %s" % (app_database, app_password))

querys = [
  "GRANT ALL PRIVILEGES ON DATABASE %s TO %s" % (app_database, app_user),
  "ALTER DATABASE %s OWNER TO %s" % (app_database, app_user),
  "GRANT CONNECT ON DATABASE %s TO role_name_ro" % app_database,
  "GRANT CONNECT ON DATABASE %s TO role_name_rw" % app_database
]
execute_querys(querys)
cursor.close()

# Admin user in app name conn
cursor = create_conn(host, app_database, admin_user, admin_pass)

querys = [
  "GRANT USAGE ON SCHEMA \"public\" TO role_name_ro",
  "GRANT USAGE, CREATE ON SCHEMA \"public\" TO role_name_rw",
  "REVOKE CREATE ON SCHEMA \"public\" FROM role_name_ro"
]
execute_querys(querys)
cursor.close()

# App user conn
cursor = create_conn(host, app_database, app_user, app_password)

querys = [
  "GRANT SELECT ON ALL TABLES IN SCHEMA \"public\" TO role_name_ro;",
  "ALTER DEFAULT PRIVILEGES IN SCHEMA \"public\" GRANT SELECT ON TABLES TO role_name_ro;",
  "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA \"public\" TO role_name_rw;",
  "ALTER DEFAULT PRIVILEGES IN SCHEMA \"public\" GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_name_rw;",
  "GRANT USAGE ON ALL SEQUENCES IN SCHEMA \"public\" TO role_name_rw;",
  "ALTER DEFAULT PRIVILEGES IN SCHEMA \"public\" GRANT USAGE ON SEQUENCES TO role_name_rw;"
]
execute_querys(querys)
cursor.close()