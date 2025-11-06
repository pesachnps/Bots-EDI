"""
Cleanup Activity Logs
Management command to remove old activity logs
"""

from django.core.management.base import BaseCommand
from usersys.activity_logger import ActivityLogger


class Command(BaseCommand):
    help = 'Clean up activity logs older than specified days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Delete logs older than this many days (default: 90)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        
        self.stdout.write(f'Cleaning up activity logs older than {days} days...')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No data will be deleted'))
            from django.utils import timezone
            from datetime import timedelta
            from usersys.partner_models import ActivityLog
            
            cutoff_date = timezone.now() - timedelta(days=days)
            count = ActivityLog.objects.filter(timestamp__lt=cutoff_date).count()
            
            self.stdout.write(
                self.style.WARNING(f'Would delete {count} activity logs')
            )
        else:
            deleted_count = ActivityLogger.cleanup_old_logs(days=days)
            
            self.stdout.write(
                self.style.SUCCESS(f'Deleted {deleted_count} activity logs')
            )
        
        self.stdout.write(self.style.SUCCESS('Cleanup complete!'))
