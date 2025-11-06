"""
User Management Service
Handles creation, update, and management of partner users
"""

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.core.exceptions import ValidationError

from .partner_models import PartnerUser, PartnerPermission, Partner
from .partner_auth_utils import PasswordValidator
from .email_service import EmailService


class UserManager:
    """Service for managing partner users"""
    
    @staticmethod
    @transaction.atomic
    def create_user(partner_id, username, email, password, first_name, last_name, 
                   role='partner_user', phone='', created_by=None, send_email=True):
        """
        Create a new partner user
        
        Args:
            partner_id: UUID of the partner
            username: Unique username
            email: User email
            password: Plain text password (will be hashed)
            first_name: First name
            last_name: Last name
            role: User role (partner_admin, partner_user, partner_readonly)
            phone: Phone number (optional)
            created_by: Admin user who created this user (optional)
            send_email: Whether to send welcome email (default: True)
        
        Returns:
            tuple: (PartnerUser instance, plain text password)
        
        Raises:
            ValidationError: If validation fails
        """
        # Validate partner exists
        try:
            partner = Partner.objects.get(id=partner_id)
        except Partner.DoesNotExist:
            raise ValidationError(f"Partner with ID {partner_id} does not exist")
        
        # Validate username uniqueness
        if PartnerUser.objects.filter(username=username).exists():
            raise ValidationError(f"Username '{username}' already exists")
        
        # Validate email format
        if not email or '@' not in email:
            raise ValidationError("Invalid email address")
        
        # Validate password
        is_valid, error_msg = PasswordValidator.validate(password)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Validate role
        valid_roles = ['partner_admin', 'partner_user', 'partner_readonly']
        if role not in valid_roles:
            raise ValidationError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        # Create user
        user = PartnerUser.objects.create(
            partner=partner,
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=make_password(password),
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            phone=phone.strip(),
            role=role,
            is_active=True,
            created_by=created_by
        )
        
        # Create permissions based on role
        default_permissions = user.get_default_permissions()
        PartnerPermission.objects.create(
            user=user,
            **default_permissions
        )
        
        # Send welcome email with credentials
        if send_email:
            EmailService.send_account_created_email(user, password)
        
        return user, password
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """
        Update a partner user
        
        Args:
            user_id: ID of the user to update
            **kwargs: Fields to update (email, first_name, last_name, phone, role, is_active)
        
        Returns:
            PartnerUser: Updated user instance
        
        Raises:
            ValidationError: If validation fails
        """
        try:
            user = PartnerUser.objects.get(id=user_id)
        except PartnerUser.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")
        
        # Update allowed fields
        if 'email' in kwargs:
            email = kwargs['email'].strip().lower()
            if not email or '@' not in email:
                raise ValidationError("Invalid email address")
            user.email = email
        
        if 'first_name' in kwargs:
            user.first_name = kwargs['first_name'].strip()
        
        if 'last_name' in kwargs:
            user.last_name = kwargs['last_name'].strip()
        
        if 'phone' in kwargs:
            user.phone = kwargs['phone'].strip()
        
        if 'role' in kwargs:
            valid_roles = ['partner_admin', 'partner_user', 'partner_readonly']
            if kwargs['role'] not in valid_roles:
                raise ValidationError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
            user.role = kwargs['role']
            
            # Update permissions to match new role
            if hasattr(user, 'permissions'):
                default_permissions = user.get_default_permissions()
                for key, value in default_permissions.items():
                    setattr(user.permissions, key, value)
                user.permissions.save()
        
        if 'is_active' in kwargs:
            user.is_active = bool(kwargs['is_active'])
        
        user.save()
        return user
    
    @staticmethod
    def reset_password(user_id, new_password):
        """
        Reset a user's password (admin action)
        
        Args:
            user_id: ID of the user
            new_password: New plain text password
        
        Returns:
            PartnerUser: Updated user instance
        
        Raises:
            ValidationError: If validation fails
        """
        try:
            user = PartnerUser.objects.get(id=user_id)
        except PartnerUser.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")
        
        # Validate password
        is_valid, error_msg = PasswordValidator.validate(new_password)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Update password
        user.password_hash = make_password(new_password)
        user.failed_login_attempts = 0
        user.locked_until = None
        user.save(update_fields=['password_hash', 'failed_login_attempts', 'locked_until'])
        
        return user
    
    @staticmethod
    def delete_user(user_id):
        """
        Delete a partner user
        
        Args:
            user_id: ID of the user to delete
        
        Returns:
            bool: True if deleted
        
        Raises:
            ValidationError: If user doesn't exist
        """
        try:
            user = PartnerUser.objects.get(id=user_id)
            user.delete()
            return True
        except PartnerUser.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")
    
    @staticmethod
    def activate_user(user_id):
        """Activate a user account"""
        try:
            user = PartnerUser.objects.get(id=user_id)
            user.is_active = True
            user.save(update_fields=['is_active'])
            return user
        except PartnerUser.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")
    
    @staticmethod
    def deactivate_user(user_id):
        """Deactivate a user account"""
        try:
            user = PartnerUser.objects.get(id=user_id)
            user.is_active = False
            user.save(update_fields=['is_active'])
            return user
        except PartnerUser.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")
    
    @staticmethod
    def get_partner_users(partner_id):
        """
        Get all users for a partner
        
        Args:
            partner_id: UUID of the partner
        
        Returns:
            QuerySet: Partner users
        """
        return PartnerUser.objects.filter(partner_id=partner_id).select_related('partner', 'permissions')
    
    @staticmethod
    def get_user_by_username(username):
        """
        Get user by username
        
        Args:
            username: Username to search for
        
        Returns:
            PartnerUser or None
        """
        try:
            return PartnerUser.objects.select_related('partner', 'permissions').get(username=username)
        except PartnerUser.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email
        
        Args:
            email: Email to search for
        
        Returns:
            PartnerUser or None
        """
        try:
            return PartnerUser.objects.select_related('partner', 'permissions').get(email__iexact=email)
        except PartnerUser.DoesNotExist:
            return None
    
    @staticmethod
    def update_permissions(user_id, permissions_dict):
        """
        Update user permissions
        
        Args:
            user_id: ID of the user
            permissions_dict: Dictionary of permissions to update
                {
                    'can_view_transactions': True,
                    'can_upload_files': False,
                    ...
                }
        
        Returns:
            PartnerPermission: Updated permissions
        
        Raises:
            ValidationError: If user doesn't exist
        """
        try:
            user = PartnerUser.objects.get(id=user_id)
        except PartnerUser.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")
        
        # Get or create permissions
        permissions, created = PartnerPermission.objects.get_or_create(
            user=user,
            defaults=user.get_default_permissions()
        )
        
        # Update permissions
        valid_permissions = [
            'can_view_transactions',
            'can_upload_files',
            'can_download_files',
            'can_view_reports',
            'can_manage_settings'
        ]
        
        for key, value in permissions_dict.items():
            if key in valid_permissions:
                setattr(permissions, key, bool(value))
        
        permissions.save()
        return permissions
    
    @staticmethod
    def get_user_stats(user_id):
        """
        Get statistics for a user
        
        Args:
            user_id: ID of the user
        
        Returns:
            dict: User statistics
        """
        try:
            user = PartnerUser.objects.get(id=user_id)
        except PartnerUser.DoesNotExist:
            return {}
        
        from .activity_logger import ActivityLogger
        
        # Get activity count
        activity_count = ActivityLogger.get_user_activity('partner', user.id, limit=1000).count()
        
        # Get login count
        login_count = ActivityLogger.get_action_count('login', user_type='partner', days=30)
        
        return {
            'total_activities': activity_count,
            'login_count_30d': login_count,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'account_age_days': (user.created_at - user.created_at).days if user.created_at else 0,
            'is_active': user.is_active,
            'is_locked': user.is_locked(),
            'failed_attempts': user.failed_login_attempts,
        }
