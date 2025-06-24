-- database/create_database.sql
SELECT 'CREATE DATABASE mantenimiento_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mantenimiento_db')\gexec