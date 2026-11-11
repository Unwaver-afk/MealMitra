from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from plans.models import TiffinPlan, Tag
from orders.models import Order, Delivery
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds initial meal plans, tags, demo users, and sample orders'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting MealMitra database seeding...'))

        # 1. Create Tags (Many-to-Many demonstration)
        tags_data = [
            ("Popular", "Most ordered and highly rated by customers"),
            ("Healthy", "Nutritionally balanced and calorie conscious"),
            ("Vegetarian", "Pure vegetarian meal options"),
            ("South Indian", "Traditional South Indian flavours and items"),
            ("Homestyle", "Simple, comforting home-cooked taste"),
            ("High Protein", "Extra paneer, lentils, and protein rich ingredients"),
            ("Budget Friendly", "Economical daily nutrition plans"),
        ]
        created_tags = {}
        for name, desc in tags_data:
            tag, _ = Tag.objects.get_or_create(name=name, defaults={'description': desc})
            created_tags[name] = tag
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_tags)} tags.'))

        # 2. Create Users
        # Admin User
        admin_email = 'admin@mealmitra.com'
        admin_user = User.objects.filter(email=admin_email).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                email=admin_email,
                password='admin123456',
                name='MealMitra Administrator'
            )
            admin_user.role = 'admin'
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_email} / admin123456'))
        else:
            self.stdout.write(self.style.NOTICE(f'Admin user already exists: {admin_email}'))

        # Demo Customer User
        customer_email = 'customer@mealmitra.com'
        customer_user = User.objects.filter(email=customer_email).first()
        if not customer_user:
            customer_user = User.objects.create_user(
                email=customer_email,
                password='user123456',
                name='Rahul Sharma'
            )
            customer_user.role = 'user'
            customer_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created demo customer: {customer_email} / user123456'))
        else:
            self.stdout.write(self.style.NOTICE(f'Demo customer already exists: {customer_email}'))

        # 3. Seed 18 Tiffin Plans (Exact match from legacy seed.js)
        plans_data = [
            # ── BREAKFAST · DAILY ──
            {
                "title": "Classic Breakfast",
                "description": "Poha with peas, a seasonal sabzi, and a glass of warm milk.",
                "meal_type": "Breakfast",
                "duration": "Daily",
                "price": 80,
                "tag_names": ["Popular", "Homestyle", "Vegetarian", "Budget Friendly"]
            },
            {
                "title": "South Indian Breakfast",
                "description": "2 idlis with sambar, coconut chutney, and filter coffee.",
                "meal_type": "Breakfast",
                "duration": "Daily",
                "price": 90,
                "tag_names": ["South Indian", "Healthy", "Vegetarian"]
            },

            # ── BREAKFAST · WEEKLY ──
            {
                "title": "Classic Breakfast",
                "description": "Poha with peas, a seasonal sabzi, and a glass of warm milk.",
                "meal_type": "Breakfast",
                "duration": "Weekly",
                "price": 499,
                "tag_names": ["Popular", "Homestyle", "Vegetarian"]
            },
            {
                "title": "South Indian Breakfast",
                "description": "2 idlis with sambar, coconut chutney, and filter coffee.",
                "meal_type": "Breakfast",
                "duration": "Weekly",
                "price": 559,
                "tag_names": ["South Indian", "Healthy", "Vegetarian"]
            },

            # ── BREAKFAST · MONTHLY ──
            {
                "title": "Classic Breakfast",
                "description": "Poha with peas, a seasonal sabzi, and a glass of warm milk.",
                "meal_type": "Breakfast",
                "duration": "Monthly",
                "price": 1799,
                "tag_names": ["Popular", "Budget Friendly", "Vegetarian"]
            },
            {
                "title": "South Indian Breakfast",
                "description": "2 idlis with sambar, coconut chutney, and filter coffee.",
                "meal_type": "Breakfast",
                "duration": "Monthly",
                "price": 1999,
                "tag_names": ["South Indian", "Healthy", "Vegetarian"]
            },

            # ── LUNCH · DAILY ──
            {
                "title": "Homestyle Lunch",
                "description": "2 rotis, dal tadka, seasonal sabzi, steamed rice, and pickle.",
                "meal_type": "Lunch",
                "duration": "Daily",
                "price": 120,
                "tag_names": ["Homestyle", "Popular", "Vegetarian"]
            },
            {
                "title": "Premium Lunch",
                "description": "3 rotis, paneer sabzi, dal makhani, rice, salad, and curd.",
                "meal_type": "Lunch",
                "duration": "Daily",
                "price": 160,
                "tag_names": ["High Protein", "Popular", "Vegetarian"]
            },

            # ── LUNCH · WEEKLY ──
            {
                "title": "Homestyle Lunch",
                "description": "2 rotis, dal tadka, seasonal sabzi, steamed rice, and pickle.",
                "meal_type": "Lunch",
                "duration": "Weekly",
                "price": 749,
                "tag_names": ["Homestyle", "Popular", "Budget Friendly"]
            },
            {
                "title": "Premium Lunch",
                "description": "3 rotis, paneer sabzi, dal makhani, rice, salad, and curd.",
                "meal_type": "Lunch",
                "duration": "Weekly",
                "price": 999,
                "tag_names": ["High Protein", "Popular", "Vegetarian"]
            },

            # ── LUNCH · MONTHLY ──
            {
                "title": "Homestyle Lunch",
                "description": "2 rotis, dal tadka, seasonal sabzi, steamed rice, and pickle.",
                "meal_type": "Lunch",
                "duration": "Monthly",
                "price": 2699,
                "tag_names": ["Homestyle", "Budget Friendly", "Popular"]
            },
            {
                "title": "Premium Lunch",
                "description": "3 rotis, paneer sabzi, dal makhani, rice, salad, and curd.",
                "meal_type": "Lunch",
                "duration": "Monthly",
                "price": 3599,
                "tag_names": ["High Protein", "Popular", "Vegetarian"]
            },

            # ── DINNER · DAILY ──
            {
                "title": "Light Dinner",
                "description": "2 rotis, dal, a light sabzi, and curd.",
                "meal_type": "Dinner",
                "duration": "Daily",
                "price": 110,
                "tag_names": ["Healthy", "Homestyle", "Vegetarian"]
            },
            {
                "title": "Hearty Dinner",
                "description": "3 rotis, shahi paneer or chicken curry, rice, raita, and salad.",
                "meal_type": "Dinner",
                "duration": "Daily",
                "price": 150,
                "tag_names": ["Popular", "High Protein"]
            },

            # ── DINNER · WEEKLY ──
            {
                "title": "Light Dinner",
                "description": "2 rotis, dal, a light sabzi, and curd.",
                "meal_type": "Dinner",
                "duration": "Weekly",
                "price": 699,
                "tag_names": ["Healthy", "Budget Friendly", "Vegetarian"]
            },
            {
                "title": "Hearty Dinner",
                "description": "3 rotis, shahi paneer or chicken curry, rice, raita, and salad.",
                "meal_type": "Dinner",
                "duration": "Weekly",
                "price": 929,
                "tag_names": ["Popular", "High Protein"]
            },

            # ── DINNER · MONTHLY ──
            {
                "title": "Light Dinner",
                "description": "2 rotis, dal, a light sabzi, and curd.",
                "meal_type": "Dinner",
                "duration": "Monthly",
                "price": 2499,
                "tag_names": ["Healthy", "Budget Friendly", "Vegetarian"]
            },
            {
                "title": "Hearty Dinner",
                "description": "3 rotis, shahi paneer or chicken curry, rice, raita, and salad.",
                "meal_type": "Dinner",
                "duration": "Monthly",
                "price": 3299,
                "tag_names": ["Popular", "High Protein"]
            },
        ]

        seeded_plans = 0
        for item in plans_data:
            tag_names = item.pop("tag_names", [])
            plan, created = TiffinPlan.objects.get_or_create(
                title=item["title"],
                meal_type=item["meal_type"],
                duration=item["duration"],
                defaults={
                    "description": item["description"],
                    "price": item["price"],
                }
            )
            # Associate tags (Many-to-Many)
            for t_name in tag_names:
                if t_name in created_tags:
                    plan.tags.add(created_tags[t_name])

            if created:
                seeded_plans += 1

        self.stdout.write(self.style.SUCCESS(f'Processed {len(plans_data)} plans (created {seeded_plans} new).'))

        # 4. Create Sample Orders for Demo Customer if none exist
        if Order.objects.filter(user=customer_user).count() == 0:
            plan_homestyle = TiffinPlan.objects.filter(title="Homestyle Lunch", duration="Weekly").first()
            if plan_homestyle:
                order_active = Order.objects.create(
                    user=customer_user,
                    plan=plan_homestyle,
                    payment_status='Paid',
                    order_status='Preparing',
                    razorpay_order_id='order_mock_demo_101',
                    razorpay_payment_id='pay_mock_demo_101'
                )
                order_active.generate_deliveries()
                self.stdout.write(self.style.SUCCESS(f'Created sample active order #{order_active.id}'))

            plan_dinner = TiffinPlan.objects.filter(title="Light Dinner", duration="Daily").first()
            if plan_dinner:
                order_completed = Order.objects.create(
                    user=customer_user,
                    plan=plan_dinner,
                    payment_status='Paid',
                    order_status='Delivered',
                    razorpay_order_id='order_mock_demo_102',
                    razorpay_payment_id='pay_mock_demo_102'
                )
                order_completed.generate_deliveries()
                self.stdout.write(self.style.SUCCESS(f'Created sample completed order #{order_completed.id}'))

        self.stdout.write(self.style.SUCCESS('MealMitra database seeding completed successfully!'))
