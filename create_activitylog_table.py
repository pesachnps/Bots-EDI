#!/usr/bin/env python
"""Directly create missing usersys tables: PartnerUser, ActivityLog, PasswordResetToken, PartnerPermission"""
import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, 'env', 'botssys', 'sqlitedb', 'botsdb')

print(f"Connecting to database: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Create PartnerUser table
    print("Creating usersys_partneruser table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usersys_partneruser (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(254) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            role VARCHAR(20) NOT NULL DEFAULT 'partner_user',
            is_active INTEGER NOT NULL DEFAULT 1,
            last_login DATETIME,
            failed_login_attempts INTEGER NOT NULL DEFAULT 0,
            locked_until DATETIME,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            created_by_id INTEGER,
            partner_id VARCHAR(16) NOT NULL,
            FOREIGN KEY (created_by_id) REFERENCES auth_user(id),
            FOREIGN KEY (partner_id) REFERENCES usersys_partner(id)
        )
    ''')
    
    # Create indexes for PartnerUser (only if they don't exist)
    print("Creating indexes for usersys_partneruser...")
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS usersys_par_partner_idx ON usersys_partneruser(partner_id, is_active)')
    except sqlite3.OperationalError:
        print("  Index usersys_par_partner_idx already exists, skipping...")
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS usersys_par_usernam_idx ON usersys_partneruser(username)')
    except sqlite3.OperationalError:
        print("  Index usersys_par_usernam_idx already exists, skipping...")
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS usersys_par_email_idx ON usersys_partneruser(email)')
    except sqlite3.OperationalError:
        print("  Index usersys_par_email_idx already exists, skipping...")
    
    # Create PartnerPermission table
    print("Creating usersys_partnerpermission table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usersys_partnerpermission (
            user_id INTEGER PRIMARY KEY,
            can_view_transactions INTEGER NOT NULL DEFAULT 1,
            can_upload_files INTEGER NOT NULL DEFAULT 0,
            can_download_files INTEGER NOT NULL DEFAULT 1,
            can_view_reports INTEGER NOT NULL DEFAULT 1,
            can_manage_settings INTEGER NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usersys_partneruser(id) ON DELETE CASCADE
        )
    ''')
    
    # Create ActivityLog table
    print("Creating usersys_activitylog table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usersys_activitylog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            user_type VARCHAR(20) NOT NULL,
            user_id INTEGER NOT NULL,
            user_name VARCHAR(100) NOT NULL,
            action VARCHAR(50) NOT NULL,
            resource_type VARCHAR(50),
            resource_id VARCHAR(100),
            details TEXT,
            ip_address VARCHAR(39),
            user_agent VARCHAR(500)
        )
    ''')
    
    # Create indexes for ActivityLog
    print("Creating indexes for usersys_activitylog...")
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS usersys_act_timesta_idx ON usersys_activitylog(timestamp DESC)')
    except sqlite3.OperationalError:
        print("  Index usersys_act_timesta_idx already exists, skipping...")
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS usersys_act_user_ty_idx ON usersys_activitylog(user_type, user_id)')
    except sqlite3.OperationalError:
        print("  Index usersys_act_user_ty_idx already exists, skipping...")
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS usersys_act_action_idx ON usersys_activitylog(action)')
    except sqlite3.OperationalError:
        print("  Index usersys_act_action_idx already exists, skipping...")
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS usersys_act_resourc_idx ON usersys_activitylog(resource_type, resource_id)')
    except sqlite3.OperationalError:
        print("  Index usersys_act_resourc_idx already exists, skipping...")
    
    # Create PasswordResetToken table
    print("Creating usersys_passwordresettoken table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usersys_passwordresettoken (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token VARCHAR(255) NOT NULL UNIQUE,
            created_at DATETIME NOT NULL,
            expires_at DATETIME NOT NULL,
            used INTEGER NOT NULL DEFAULT 0,
            used_at DATETIME,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usersys_partneruser(id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for PasswordResetToken
    print("Creating indexes for usersys_passwordresettoken...")
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS usersys_pas_token_idx ON usersys_passwordresettoken(token)')
    except sqlite3.OperationalError:
        print("  Index usersys_pas_token_idx already exists, skipping...")
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS usersys_pas_user_id_idx ON usersys_passwordresettoken(user_id, created_at DESC)')
    except sqlite3.OperationalError:
        print("  Index usersys_pas_user_id_idx already exists, skipping...")
    
    # Commit all changes
    conn.commit()
    print("\n✅ All tables created successfully!")
    
    # Verify tables were created
    print("\n=== Verifying tables ===")
    tables_to_check = ['usersys_partneruser', 'usersys_partnerpermission', 'usersys_activitylog', 'usersys_passwordresettoken']
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables_to_check:
        if table in existing_tables:
            print(f"  ✓ {table}")
        else:
            print(f"  ✗ {table} - MISSING!")
    
    # Now mark migration 0004 as applied
    print("\n=== Marking migration as applied ===")
    cursor.execute('''
        INSERT OR IGNORE INTO django_migrations (app, name, applied)
        VALUES ('usersys', '0004_partner_users_permissions', datetime('now'))
    ''')
    conn.commit()
    print("  ✓ Migration 0004 marked as applied")
    
except Exception as e:
    print(f"\n❌ Error creating tables: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

print("\n✅ Done!")
