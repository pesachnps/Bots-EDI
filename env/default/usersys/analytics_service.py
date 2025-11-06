"""
Analytics Service
Calculates metrics, statistics, and generates chart data for dashboards
"""

from django.db.models import Count, Q, Avg, Sum
from django.utils import timezone
from datetime import timedelta, datetime
from collections import defaultdict

from .partner_models import Partner
from .modern_edi_models import EDITransaction


class AnalyticsService:
    """Service for calculating analytics and metrics"""
    
    @staticmethod
    def get_dashboard_metrics(days=30):
        """
        Get key metrics for admin dashboard
        
        Args:
            days: Number of days to look back (default: 30)
        
        Returns:
            dict: Dashboard metrics
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Total partners
        total_partners = Partner.objects.filter(status='active').count()
        
        # Total transactions
        total_transactions = EDITransaction.objects.filter(
            created_at__gte=cutoff_date
        ).count()
        
        # Success/error rates
        sent_transactions = EDITransaction.objects.filter(
            folder='sent',
            sent_at__gte=cutoff_date
        )
        
        total_sent = sent_transactions.count()
        acknowledged = sent_transactions.filter(acknowledgment_status='acknowledged').count()
        failed = sent_transactions.filter(acknowledgment_status='rejected').count()
        
        success_rate = (acknowledged / total_sent * 100) if total_sent > 0 else 0
        error_rate = (failed / total_sent * 100) if total_sent > 0 else 0
        
        return {
            'total_partners': total_partners,
            'total_transactions': total_transactions,
            'success_rate': round(success_rate, 1),
            'error_rate': round(error_rate, 1),
            'total_sent': total_sent,
            'acknowledged': acknowledged,
            'failed': failed,
            'pending': total_sent - acknowledged - failed,
        }
    
    @staticmethod
    def get_transaction_volume_chart(days=30):
        """
        Get transaction volume data for chart
        
        Args:
            days: Number of days to include
        
        Returns:
            list: Daily transaction counts
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Get transactions grouped by date
        transactions = EDITransaction.objects.filter(
            created_at__gte=cutoff_date
        ).extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Create a dict for easy lookup
        transaction_dict = {item['date']: item['count'] for item in transactions}
        
        # Generate data for all days (fill in zeros for missing days)
        result = []
        for i in range(days):
            date = (timezone.now() - timedelta(days=days-i-1)).date()
            date_str = date.isoformat()
            result.append({
                'date': date_str,
                'count': transaction_dict.get(date, 0)
            })
        
        return result
    
    @staticmethod
    def get_top_partners(limit=10, days=30):
        """
        Get top partners by transaction volume
        
        Args:
            limit: Number of partners to return
            days: Number of days to look back
        
        Returns:
            list: Top partners with transaction counts
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Get transaction counts per partner
        partner_counts = EDITransaction.objects.filter(
            created_at__gte=cutoff_date,
            partner_id__isnull=False
        ).values('partner_id', 'partner_name').annotate(
            transaction_count=Count('id')
        ).order_by('-transaction_count')[:limit]
        
        return list(partner_counts)
    
    @staticmethod
    def get_recent_errors(limit=10):
        """
        Get recent transaction errors
        
        Args:
            limit: Number of errors to return
        
        Returns:
            list: Recent errors
        """
        errors = EDITransaction.objects.filter(
            Q(acknowledgment_status='rejected') | Q(folder='deleted')
        ).select_related('partner_links').order_by('-modified_at')[:limit]
        
        result = []
        for txn in errors:
            result.append({
                'id': str(txn.id),
                'partner_name': txn.partner_name or 'Unknown',
                'document_type': txn.document_type,
                'error_type': txn.acknowledgment_status or 'Processing Error',
                'error_message': txn.acknowledgment_message or 'No details available',
                'timestamp': txn.modified_at.isoformat(),
            })
        
        return result
    
    @staticmethod
    def get_system_status():
        """
        Get system health status indicators
        
        Returns:
            dict: System status
        """
        # Check recent activity
        recent_transactions = EDITransaction.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=1)
        ).count()
        
        # Check for stuck transactions
        stuck_transactions = EDITransaction.objects.filter(
            folder='outbox',
            created_at__lt=timezone.now() - timedelta(hours=24)
        ).count()
        
        # Database health (simple check)
        try:
            Partner.objects.count()
            database_status = 'healthy'
        except Exception:
            database_status = 'error'
        
        return {
            'database': database_status,
            'api_services': 'healthy',  # Could add actual health checks
            'sftp_polling': 'healthy',  # Could check last poll time
            'recent_activity': recent_transactions > 0,
            'stuck_transactions': stuck_transactions,
        }
    
    @staticmethod
    def get_document_type_breakdown(days=30):
        """
        Get breakdown of transactions by document type
        
        Args:
            days: Number of days to look back
        
        Returns:
            list: Document type counts
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        breakdown = EDITransaction.objects.filter(
            created_at__gte=cutoff_date
        ).values('document_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return list(breakdown)
    
    @staticmethod
    def get_partner_success_rates(days=30):
        """
        Get success/failure rates by partner
        
        Args:
            days: Number of days to look back
        
        Returns:
            list: Partner success rates
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        partners = Partner.objects.filter(status='active')
        result = []
        
        for partner in partners:
            sent = EDITransaction.objects.filter(
                partner_id=partner.id,
                folder='sent',
                sent_at__gte=cutoff_date
            )
            
            total = sent.count()
            if total == 0:
                continue
            
            acknowledged = sent.filter(acknowledgment_status='acknowledged').count()
            failed = sent.filter(acknowledgment_status='rejected').count()
            
            success_rate = (acknowledged / total * 100) if total > 0 else 0
            
            result.append({
                'partner_id': str(partner.id),
                'partner_name': partner.name,
                'total': total,
                'acknowledged': acknowledged,
                'failed': failed,
                'success_rate': round(success_rate, 1),
            })
        
        # Sort by total transactions
        result.sort(key=lambda x: x['total'], reverse=True)
        return result[:20]  # Top 20 partners
    
    @staticmethod
    def get_average_processing_time(days=30):
        """
        Get average processing time for transactions
        
        Args:
            days: Number of days to look back
        
        Returns:
            dict: Processing time metrics
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Calculate time from creation to sent
        sent_transactions = EDITransaction.objects.filter(
            folder='sent',
            sent_at__gte=cutoff_date,
            sent_at__isnull=False
        )
        
        total_time = timedelta()
        count = 0
        
        for txn in sent_transactions:
            if txn.created_at and txn.sent_at:
                total_time += (txn.sent_at - txn.created_at)
                count += 1
        
        avg_seconds = total_time.total_seconds() / count if count > 0 else 0
        
        return {
            'average_seconds': round(avg_seconds, 2),
            'average_minutes': round(avg_seconds / 60, 2),
            'sample_size': count,
        }
    
    @staticmethod
    def get_partner_analytics(partner_id, days=30):
        """
        Get analytics for a specific partner
        
        Args:
            partner_id: UUID of the partner
            days: Number of days to look back
        
        Returns:
            dict: Partner analytics
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        transactions = EDITransaction.objects.filter(
            partner_id=partner_id,
            created_at__gte=cutoff_date
        )
        
        total = transactions.count()
        sent = transactions.filter(folder='sent').count()
        received = transactions.filter(folder='received').count()
        pending = transactions.filter(folder__in=['inbox', 'outbox']).count()
        errors = transactions.filter(folder='deleted').count()
        
        # Document type breakdown
        doc_types = transactions.values('document_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return {
            'total_transactions': total,
            'sent': sent,
            'received': received,
            'pending': pending,
            'errors': errors,
            'document_types': list(doc_types),
        }
    
    @staticmethod
    def get_activity_heatmap(days=30):
        """
        Get activity heatmap data (hour of day × day of week)
        
        Args:
            days: Number of days to look back
        
        Returns:
            dict: Heatmap data
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        transactions = EDITransaction.objects.filter(
            created_at__gte=cutoff_date
        )
        
        # Initialize heatmap (7 days × 24 hours)
        heatmap = defaultdict(lambda: defaultdict(int))
        
        for txn in transactions:
            day_of_week = txn.created_at.weekday()  # 0=Monday, 6=Sunday
            hour = txn.created_at.hour
            heatmap[day_of_week][hour] += 1
        
        # Convert to list format
        result = []
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in range(7):
            for hour in range(24):
                result.append({
                    'day': day_names[day],
                    'hour': hour,
                    'count': heatmap[day][hour],
                })
        
        return result
