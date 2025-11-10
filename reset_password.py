#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'bots.settings'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'env', 'default', 'config'))

import django
django.setup()

from django.contrib.auth.models import User

# Reset password for bots user
try:
    user = User.objects.get(username='bots')
    user.set_password('bots')
    user.save()
    print(f"✓ Password reset successfully for user: {user.username}")
    print(f"  Username: bots")
    print(f"  Password: bots")
except User.DoesNotExist:
    print("✗ User 'bots' not found")
    print("\nCreating user 'bots'...")
    user = User.objects.create_superuser('bots', 'bots@example.com', 'bots')
    print(f"✓ User created successfully")
    print(f"  Username: bots")
    print(f"  Password: bots")
