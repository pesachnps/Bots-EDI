"""
Initialize Partner Portal
Management command to set up partner portal with default data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from usersys.partner_models import Partner, PartnerUser, PartnerPermission


class Command(BaseCommand):
    help = 'Initialize partner portal with default permission sets and optional sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-sample',
            action='store_true',
            help='Create sample partner users for testing',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing Partner Portal...'))
        
        # Ensure all existing users have permissions
        users_without_permissions = PartnerUser.objects.filter(permissions__isnull=True)
        created_count = 0
        
        for user in users_without_permissions:
            defaults = user.get_default_permissions()
            PartnerPermission.objects.create(user=user, **defaults)
            created_count += 1
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Created permissions for {created_count} existing users')
            )
        
        # Create sample data if requested
        if options['create_sample']:
            self.create_sample_data()
        
        self.stdout.write(self.style.SUCCESS('Partner Portal initialization complete!'))

    def create_sample_data(self):
        """Create sample partner users for testing"""
        self.stdout.write('Creating sample partner users...')
        
        # Get first active partner
        partner = Partner.objects.filter(status='active').first()
        
        if not partner:
            self.stdout.write(
                self.style.WARNING('No active partners found. Skipping sample user creation.')
            )
            return
        
        # Create sample users for each role
        sample_users = [
            {
                'username': f'{partner.partner_id.lower()}_admin',
                'email': f'admin@{partner.partner_id.lower()}.example.com',
                'password': 'Admin123!@#',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'partner_admin',
            },
            {
                'username': f'{partner.partner_id.lower()}_user',
                'email': f'user@{partner.partner_id.lower()}.example.com',
                'password': 'User123!@#',
                'first_name': 'Standard',
                'last_name': 'User',
                'role': 'partner_user',
            },
            {
                'username': f'{partner.partner_id.lower()}_readonly',
                'email': f'readonly@{partner.partner_id.lower()}.example.com',
                'password': 'Read123!@#',
                'first_name': 'ReadOnly',
                'last_name': 'User',
                'role': 'partner_readonly',
            },
        ]
        
        for user_data in sample_users:
            # Check if user already exists
            if PartnerUser.objects.filter(username=user_data['username']).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {user_data["username"]} already exists, skipping')
                )
                continue
            
            # Create user
            user = PartnerUser.objects.create(
                partner=partner,
                username=user_data['username'],
                email=user_data['email'],
                password_hash=make_password(user_data['password']),
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role'],
                is_active=True,
            )
            
            # Create permissions
            defaults = user.get_default_permissions()
            PartnerPermission.objects.create(user=user, **defaults)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {user_data["role"]} user: {user_data["username"]} '
                    f'(password: {user_data["password"]})'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Sample users created for partner: {partner.name}')
        )
