# save the database on the host so the settings are persisted after restarting the service
SQLALCHEMY_DATABASE_URI = 'sqlite:////superset/superset.db?check_same_thread=false'
