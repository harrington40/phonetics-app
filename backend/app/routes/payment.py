"""
Payment API Routes
"""
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from ..services.payment_service import (
    create_checkout_session,
    verify_checkout_session,
    cancel_subscription,
    handle_stripe_webhook
)
from ..services.email_service import send_license_key_email, send_payment_success_email
from ..services.license_service import create_license, LicenseType
from ..db.database import get_db
from ..db.models import User, License, Payment

router = APIRouter()

class CheckoutRequest(BaseModel):
    email: EmailStr
    plan_type: str  # parent_monthly, parent_yearly, teacher_monthly, teacher_yearly
    success_url: str = "http://localhost:3000/payment-success.html"
    cancel_url: str = "http://localhost:3000/landing.html#pricing"

class PaymentVerification(BaseModel):
    session_id: str

@router.post("/payment/create-checkout")
async def create_payment_checkout(request: CheckoutRequest, db: Session = Depends(get_db)):
    """
    Create a Stripe checkout session for subscription
    """
    try:
        # Create checkout session
        session_result = await create_checkout_session(
            customer_email=request.email,
            plan_type=request.plan_type,
            success_url=request.success_url,
            cancel_url=request.cancel_url
        )
        
        if not session_result.get("success"):
            raise HTTPException(status_code=400, detail=session_result.get("error"))
        
        # Create or get user
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            user = User(email=request.email, full_name=request.email.split('@')[0])
            db.add(user)
            db.commit()
            db.refresh(user)
        
        return {
            "checkout_url": session_result["url"],
            "session_id": session_result["session_id"],
            "message": "Redirect user to checkout_url to complete payment"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/payment/verify")
async def verify_payment(request: PaymentVerification, db: Session = Depends(get_db)):
    """
    Verify payment and create license after successful checkout
    """
    try:
        # Verify session
        session_data = await verify_checkout_session(request.session_id)
        
        if not session_data:
            raise HTTPException(status_code=400, detail="Invalid or unpaid session")
        
        # Get user
        user = db.query(User).filter(User.email == session_data["email"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Determine license type and duration from plan
        plan_type = session_data.get("plan_type", "parent_monthly")
        
        if "parent" in plan_type:
            license_type = LicenseType.PARENT
        elif "teacher" in plan_type:
            license_type = LicenseType.TEACHER
        else:
            license_type = LicenseType.PARENT
        
        duration_days = 365 if "yearly" in plan_type else 30
        
        # Create license
        license = create_license(
            email=session_data["email"],
            license_type=license_type,
            duration_days=duration_days
        )
        
        # Save license to database
        db_license = License(
            license_key=license.license_key,
            license_type=license.license_type.value,
            user_id=user.id,
            start_date=license.start_date,
            end_date=license.end_date,
            is_active=True,
            max_students=license.max_students,
            max_lessons=license.features.max_lessons,
            features=license.features.dict(),
            stripe_subscription_id=session_data.get("subscription_id")
        )
        db.add(db_license)
        
        # Record payment
        payment = Payment(
            user_id=user.id,
            amount=session_data.get("amount_total", 0),
            currency="USD",
            payment_method="stripe",
            payment_status="completed",
            stripe_payment_id=request.session_id,
            license_type=license_type.value,
            metadata={"plan_type": plan_type}
        )
        db.add(payment)
        db.commit()
        
        # Send email with license key
        await send_payment_success_email(
            to_email=session_data["email"],
            amount=session_data.get("amount_total", 0),
            plan_type=plan_type,
            license_key=license.license_key
        )
        
        return {
            "success": True,
            "license_key": license.license_key,
            "license_type": license_type.value,
            "end_date": license.end_date.isoformat(),
            "message": "Payment successful! License created and email sent."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/payment/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Stripe webhook events
    """
    try:
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")
        
        event = handle_stripe_webhook(payload, sig_header)
        
        if not event:
            raise HTTPException(status_code=400, detail="Invalid webhook")
        
        event_type = event["type"]
        event_data = event["data"]
        
        # Handle different event types
        if event_type == "checkout.session.completed":
            # Payment successful
            customer_email = event_data.get("customer_email")
            subscription_id = event_data.get("subscription")
            print(f"✅ Payment completed for {customer_email}")
            
        elif event_type == "customer.subscription.deleted":
            # Subscription canceled
            subscription_id = event_data.get("id")
            
            # Deactivate license
            license = db.query(License).filter(
                License.stripe_subscription_id == subscription_id
            ).first()
            
            if license:
                license.is_active = False
                db.commit()
                print(f"❌ License {license.license_key} deactivated")
                
        elif event_type == "invoice.payment_failed":
            # Payment failed
            customer_email = event_data.get("customer_email")
            print(f"⚠️ Payment failed for {customer_email}")
        
        return {"received": True}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/payment/cancel-subscription")
async def cancel_user_subscription(subscription_id: str, db: Session = Depends(get_db)):
    """
    Cancel a subscription
    """
    try:
        success = await cancel_subscription(subscription_id)
        
        if success:
            # Update license in database
            license = db.query(License).filter(
                License.stripe_subscription_id == subscription_id
            ).first()
            
            if license:
                license.is_active = False
                db.commit()
            
            return {"success": True, "message": "Subscription canceled"}
        else:
            raise HTTPException(status_code=400, detail="Failed to cancel subscription")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
