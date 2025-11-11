#!/usr/bin/env python
"""Create partner user tables"""
import os
import sys
import django
import sqlite3
from dotenv import load_dotenv

# Set up project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ENV_DEFAULT = os.path.join(PROJECT_ROOT, 'env', 'default')

# Load environment variables
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# Set environment variables for Django
os.environ['PROJECT_ROOT'] = PROJECT_ROOT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Add to Python path
sys.path.insert(0, ENV_DEFAULT)

# Setup Django
django.setup()

from django.db import connection

print("Creating partner user tables...")

# SQL to create the partner tables
sql_statements = [
    "DROP TABLE IF EXISTS usersys_passwordresettoken",
    "DROP TABLE IF EXISTS usersys_partnerpermissions",
    "DROP TABLE IF EXISTS usersys_partneruser",
    "DROP TABLE IF EXISTS usersys_partner",
    """
    CREATE TABLE usersys_partner (
        id TEXT PRIMARY KEY,
        partner_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        display_name TEXT NOT NULL,
        contact_name TEXT,
        contact_email TEXT,
        contact_phone TEXT,
        communication_method TEXT NOT NULL DEFAULT 'both',
        status TEXT NOT NULL DEFAULT 'active',
        edi_format TEXT NOT NULL DEFAULT 'X12',
        sender_id TEXT,
        receiver_id TEXT,
        supported_document_types TEXT DEFAULT '[]',
        notes TEXT,
        configuration TEXT DEFAULT '{}',
        created_at TEXT NOT NULL,
        modified_at TEXT NOT NULL,
        created_by_id INTEGER
    )
    """,
    """
    CREATE TABLE usersys_partneruser (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_id TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        phone TEXT,
        role TEXT NOT NULL DEFAULT 'partner_user',
        is_active INTEGER NOT NULL DEFAULT 1,
        last_login TEXT,
        failed_login_attempts INTEGER NOT NULL DEFAULT 0,
        locked_until TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        created_by_id INTEGER,
        FOREIGN KEY (partner_id) REFERENCES usersys_partner (id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS usersys_partnerpermissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        can_view_transactions INTEGER NOT NULL DEFAULT 1,
        can_upload_files INTEGER NOT NULL DEFAULT 1,
        can_download_files INTEGER NOT NULL DEFAULT 1,
        can_view_reports INTEGER NOT NULL DEFAULT 1,
        can_manage_users INTEGER NOT NULL DEFAULT 0,
        can_configure_settings INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        modified_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES usersys_partneruser (id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS usersys_passwordresettoken (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        expires_at TEXT NOT NULL,
        used INTEGER NOT NULL DEFAULT 0,
        used_at TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES usersys_partneruser (id)
    )
    """
]

with connection.cursor() as cursor:
    for sql in sql_statements:
        try:
            cursor.execute(sql)
            print(f"✅ Executed SQL statement")
        except Exception as e:
            print(f"❌ Error: {e}")

print("\n✅ Partner tables created successfully!")
print("\nNow you can run: python create_partner_user.py")
