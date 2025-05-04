# reset_migrations.py
from django.db import connection

cursor = connection.cursor()
# Delete all migration records
cursor.execute("DELETE FROM django_migrations")
cursor.close()
print("Migration records deleted.")