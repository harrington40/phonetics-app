"""
Stripe Payment Integration
"""
import stripe
import os
from typing import Dict, Optional
from datetime import datetime, timedelta

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")

# Stripe Price IDs (create these in Stripe Dashboard)
STRIPE_PRICES = {
    "parent_monthly": os.getenv("STRIPE_PRICE_PARENT_MONTHLY", "price_parent_monthly"),
    "parent_yearly": os.getenv("STRIPE_PRICE_PARENT_YEARLY", "price_parent_yearly"),
    "teacher_monthly": os.getenv("STRIPE_PRICE_TEACHER_MONTHLY", "price_teacher_monthly"),
    "teacher_yearly": os.getenv("STRIPE_PRICE_TEACHER_YEARLY", "price_teacher_yearly"),
}

PLAN_PRICES = {
    "parent_monthly": 9.99,
    "parent_yearly": 99.99,
    "teacher_monthly": 29.99,
    "teacher_yearly": 299.99,
}

async def create_checkout_session(
    customer_email: str,
    plan_type: str,
    success_url: str,
    cancel_url: str
) -> Dict:
    """
    Create a Stripe checkout session for subscription
    """
    try:
        price_id = STRIPE_PRICES.get(plan_type)
        
        if not price_id:
            raise ValueError(f"Invalid plan type: {plan_type}")
        
        session = stripe.checkout.Session.create(
            customer_email=customer_email,
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            metadata={
                "plan_type": plan_type,
            }
        )
        
        return {
            "session_id": session.id,
            "url": session.url,
            "success": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

async def verify_checkout_session(session_id: str) -> Optional[Dict]:
    """
    Verify and retrieve checkout session details
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == "paid":
            return {
                "email": session.customer_email,
                "subscription_id": session.subscription,
                "plan_type": session.metadata.get("plan_type"),
                "payment_status": session.payment_status,
                "amount_total": session.amount_total / 100,  # Convert from cents
            }
        return None
    except Exception as e:
        print(f"Error verifying session: {e}")
        return None

async def cancel_subscription(subscription_id: str) -> bool:
    """
    Cancel a Stripe subscription
    """
    try:
        stripe.Subscription.delete(subscription_id)
        return True
    except Exception as e:
        print(f"Error canceling subscription: {e}")
        return False

async def create_payment_intent(amount: float, currency: str = "usd") -> Dict:
    """
    Create a payment intent for one-time payments
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            automatic_payment_methods={"enabled": True},
        )
        
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
            "success": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

async def get_subscription_status(subscription_id: str) -> Optional[Dict]:
    """
    Get subscription status from Stripe
    """
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        return {
            "status": subscription.status,
            "current_period_end": datetime.fromtimestamp(subscription.current_period_end),
            "cancel_at_period_end": subscription.cancel_at_period_end,
        }
    except Exception as e:
        print(f"Error getting subscription: {e}")
        return None

def handle_stripe_webhook(payload: bytes, sig_header: str) -> Optional[Dict]:
    """
    Handle Stripe webhook events
    """
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_...")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        
        event_type = event["type"]
        event_data = event["data"]["object"]
        
        return {
            "type": event_type,
            "data": event_data
        }
    except Exception as e:
        print(f"Webhook error: {e}")
        return None
