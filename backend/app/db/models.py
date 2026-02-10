"""
Database models for PhonicsLearn
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="student")  # student, teacher, admin
    is_active = Column(Boolean, default=True)
    has_paid = Column(Boolean, default=False)  # Payment verification for students
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # For students enrolled with a teacher
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    licenses = relationship("License", back_populates="user")
    students = relationship("Student", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    # Teacher-Student relationship
    enrolled_students = relationship("User", back_populates="teacher", foreign_keys="User.teacher_id")
    teacher = relationship("User", back_populates="enrolled_students", foreign_keys=[teacher_id], remote_side=[id])

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    license_key = Column(String, unique=True, index=True, nullable=False)
    license_type = Column(String, nullable=False)  # free_trial, parent, teacher, school
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    max_students = Column(Integer, default=3)
    max_lessons = Column(Integer, default=10)
    features = Column(JSON)
    stripe_subscription_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="licenses")
    usage_logs = relationship("UsageLog", back_populates="license")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    age = Column(Integer)
    grade_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="students")
    progress = relationship("StudentProgress", back_populates="student")
    activity_logs = relationship("ActivityLog", back_populates="student")

class StudentProgress(Base):
    __tablename__ = "student_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    lesson_id = Column(String, nullable=False)
    phoneme = Column(String, nullable=False)
    mastery_level = Column(Float, default=0.0)
    attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    last_practiced = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="progress")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    lesson_id = Column(String, nullable=False)
    activity_type = Column(String)  # lesson_start, lesson_complete, quiz, recording
    score = Column(Float, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="activity_logs")

class UsageLog(Base):
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    license_id = Column(Integer, ForeignKey("licenses.id"))
    action = Column(String, nullable=False)  # lesson_accessed, feature_used, etc.
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    license = relationship("License", back_populates="usage_logs")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    payment_method = Column(String)  # stripe, paypal
    payment_status = Column(String)  # pending, completed, failed, refunded
    stripe_payment_id = Column(String, nullable=True)
    stripe_invoice_id = Column(String, nullable=True)
    license_type = Column(String)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="payments")

class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_email = Column(String, nullable=False)
    email_type = Column(String, nullable=False)  # welcome, license_key, reminder, expiration
    subject = Column(String)
    status = Column(String)  # sent, failed, pending
    sendgrid_message_id = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TeacherClass(Base):
    __tablename__ = "teacher_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_name = Column(String, nullable=False)
    class_code = Column(String, unique=True, index=True, nullable=False)  # Used for student enrollment
    description = Column(Text, nullable=True)
    max_students = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
