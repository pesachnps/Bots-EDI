"""
Django management command to check EDI acknowledgments
"""

from django.core.management.base import BaseCommand
from usersys.acknowledgment_tracker import AcknowledgmentTracker


class Command(BaseCommand):
    help = 'Check for EDI acknowledgments for sent transactions'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--transaction-id',
            type=str,
            help='Check acknowledgment for a specific transaction',
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Display acknowledgment statistics',
        )
        parser.add_argument(
            '--retry-failed',
            action='store_true',
            help='Retry failed acknowledgment checks',
        )
    
    def handle(self, *args, **options):
        tracker = AcknowledgmentTracker()
        
        # Check specific transaction
        if options['transaction_id']:
            self.stdout.write(f"Checking acknowledgment for transaction {options['transaction_id']}...")
            result = tracker.check_single_transaction(options['transaction_id'])
            
            if 'error' in result:
                self.stdout.write(self.style.ERROR(f"Error: {result['error']}"))
            else:
                if result['acknowledged']:
                    self.stdout.write(self.style.SUCCESS(f"Transaction acknowledged: {result['status']}"))
                    self.stdout.write(f"Message: {result['message']}")
                else:
                    self.stdout.write(self.style.WARNING("Transaction not yet acknowledged"))
            
            return
        
        # Display statistics
        if options['stats']:
            self.stdout.write("Acknowledgment Statistics:")
            self.stdout.write("-" * 50)
            
            stats = tracker.get_acknowledgment_statistics()
            self.stdout.write(f"Total sent: {stats['total_sent']}")
            self.stdout.write(f"Acknowledged: {stats['acknowledged']}")
            self.stdout.write(f"Rejected: {stats['rejected']}")
            self.stdout.write(f"Pending: {stats['pending']}")
            self.stdout.write(f"Acknowledgment rate: {stats['acknowledgment_rate']:.1f}%")
            
            return
        
        # Retry failed acknowledgments
        if options['retry_failed']:
            self.stdout.write("Retrying failed acknowledgment checks...")
            result = tracker.retry_failed_acknowledgments()
            
            self.stdout.write(self.style.SUCCESS(
                f"Retried {result['retried']} transactions, {result['successful']} successful"
            ))
            
            return
        
        # Default: check all pending acknowledgments
        self.stdout.write("Checking acknowledgments for all sent transactions...")
        result = tracker.check_acknowledgments()
        
        self.stdout.write(self.style.SUCCESS(
            f"Checked {result['checked']} transactions, {result['acknowledged']} newly acknowledged"
        ))
        self.stdout.write(f"Completed at: {result['timestamp']}")
