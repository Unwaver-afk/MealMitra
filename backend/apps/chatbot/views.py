import re
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from plans.models import TiffinPlan


class ChatbotView(APIView):
    """
    POST /api/chatbot
    Simulated conversational assistant for MealMitra.
    Generates intelligent contextual recommendations directly from SQLite database records
    without calling external Google Gemini APIs or requiring SSE streaming infrastructure.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        message = (request.data.get('message') or '').strip().lower()
        if not message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Contextual response generation using local database plans
        reply = self.generate_response(message)

        return Response({
            "text": reply,
            "summary": "Customer discussed meal plan recommendations and preferences."
        }, status=status.HTTP_200_OK)

    def generate_response(self, text):
        # 1. Check for budget queries (e.g., "under 1000", "under 500", "cheap", "budget")
        budget_match = re.search(r'(?:under|below|less than|budget of)\s*(?:₹|rs\.?|inr)?\s*(\d+)', text)
        if budget_match:
            max_price = float(budget_match.group(1))
            matching_plans = TiffinPlan.objects.filter(price__lte=max_price, is_active=True).order_by('price')[:4]
            if matching_plans.exists():
                lines = [f"Here are our best meal plans fitting your budget of **₹{int(max_price)}**:\n"]
                for p in matching_plans:
                    lines.append(f"- **{p.title}** ({p.meal_type} · {p.duration}): **₹{p.price}** — {p.description}")
                lines.append("\nYou can select and subscribe to any of these plans directly from our **Plans** page!")
                return "\n".join(lines)
            else:
                cheapest = TiffinPlan.objects.filter(is_active=True).order_by('price').first()
                return f"We don't have plans under ₹{int(max_price)}, but our most affordable plan is the **{cheapest.title}** ({cheapest.meal_type} · {cheapest.duration}) starting at just **₹{cheapest.price}**!"

        # 2. Check for meal type queries
        if 'breakfast' in text:
            plans = TiffinPlan.objects.filter(meal_type='Breakfast', is_active=True).order_by('price')[:3]
            return (
                "Here are our top **Breakfast** subscription options:\n\n" +
                "\n".join([f"- **{p.title}** ({p.duration}): **₹{p.price}** — {p.description}" for p in plans]) +
                "\n\nFresh, nutritious mornings made easy with daily doorstep delivery!"
            )

        if 'lunch' in text:
            plans = TiffinPlan.objects.filter(meal_type='Lunch', is_active=True).order_by('price')[:3]
            return (
                "Looking for a wholesome midday meal? Check out our **Lunch** plans:\n\n" +
                "\n".join([f"- **{p.title}** ({p.duration}): **₹{p.price}** — {p.description}" for p in plans]) +
                "\n\nEach meal comes hot, freshly prepared, and delivered right on time."
            )

        if 'dinner' in text:
            plans = TiffinPlan.objects.filter(meal_type='Dinner', is_active=True).order_by('price')[:3]
            return (
                "Here are our recommended **Dinner** options:\n\n" +
                "\n".join([f"- **{p.title}** ({p.duration}): **₹{p.price}** — {p.description}" for p in plans]) +
                "\n\nEnjoy healthy, homemade dinners without the hassle of cooking or cleaning!"
            )

        # 3. Check for duration queries
        if 'monthly' in text or 'month' in text:
            plans = TiffinPlan.objects.filter(duration='Monthly', is_active=True).order_by('price')[:3]
            return (
                "Our **Monthly Subscriptions** offer maximum savings with hassle-free 30-day service:\n\n" +
                "\n".join([f"- **{p.title}** ({p.meal_type}): **₹{p.price}/month** — {p.description}" for p in plans]) +
                "\n\nSubscribe today and enjoy uninterrupted daily meals!"
            )

        if 'weekly' in text or 'week' in text:
            plans = TiffinPlan.objects.filter(duration='Weekly', is_active=True).order_by('price')[:3]
            return (
                "Our **Weekly Subscriptions** (7 days) are great for testing out our service:\n\n" +
                "\n".join([f"- **{p.title}** ({p.meal_type}): **₹{p.price}/week** — {p.description}" for p in plans])
            )

        # 4. Check for dietary keywords
        if 'south indian' in text or 'dosa' in text or 'idli' in text:
            plans = TiffinPlan.objects.filter(title__icontains='South Indian', is_active=True)
            return (
                "We have authentic **South Indian Breakfast** plans prepared with traditional recipes:\n\n" +
                "\n".join([f"- **{p.title}** ({p.duration}): **₹{p.price}** — {p.description}" for p in plans])
            )

        if 'veg' in text or 'vegetarian' in text:
            return (
                "All of MealMitra's daily tiffin meals are **100% vegetarian** and prepared under strict hygiene standards. "
                "You can choose from our Daily, Weekly, or Monthly packages for Breakfast, Lunch, and Dinner!"
            )

        # 5. Generic greeting or default answer
        popular_plans = TiffinPlan.objects.filter(is_active=True).order_by('price')[:3]
        plan_list = "\n".join([f"- **{p.title}** ({p.meal_type} · {p.duration}): ₹{p.price}" for p in popular_plans])

        return (
            "Hello! I am your **MealMitra Assistant**.\n\n"
            "I can help you find the ideal tiffin plan based on your dietary preferences, meal timings, or budget.\n\n"
            f"Here are a few popular plans to get started:\n{plan_list}\n\n"
            "Feel free to ask me about **Breakfast**, **Lunch**, **Dinner**, or plans under a specific budget (e.g. *'Suggest a lunch plan under ₹1000'*)."
        )
