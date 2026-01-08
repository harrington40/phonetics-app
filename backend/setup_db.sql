-- PostgreSQL Database Setup for PhonicsLearn

-- Create database
CREATE DATABASE phonicslearn;

-- Create user
CREATE USER phonicslearn WITH PASSWORD 'phonicslearn123';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE phonicslearn TO phonicslearn;

-- Connect to database
\c phonicslearn;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO phonicslearn;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO phonicslearn;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO phonicslearn;

-- The tables will be created automatically by SQLAlchemy when the app starts
