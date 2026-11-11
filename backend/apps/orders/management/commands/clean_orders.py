from django.core.management.base import BaseCommand
from orders.models import Order


class Command(BaseCommand):
    help = 'Cleans orphaned orders with missing plans or users (equivalent to legacy cleanOrders.js)'

    def handle(self, *args, **options):
        # In relational Django SQLite with CASCADE, orphaned rows are automatically handled.
        # This utility verifies order consistency.
        total_orders = Order.objects.count()
        valid_orders = Order.objects.filter(plan__isnull=False, user__isnull=False).count()
        orphaned = total_orders - valid_orders

        if orphaned > 0:
            deleted_count, _ = Order.objects.filter(plan__isnull=True).delete()
            self.stdout.write(self.style.SUCCESS(f"Cleaned {deleted_count} orphaned orders."))
        else:
            self.stdout.write(self.style.SUCCESS(f"All {total_orders} orders are healthy with valid relationships."))
