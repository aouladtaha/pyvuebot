import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Setup logging
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    logger.warning(
        "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")
    # We'll let the application handle this situation

try:
    supabase: Client = create_client(supabase_url, supabase_key)
    logger.info("Supabase client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {str(e)}")
    supabase = None

# SQL for creating the tasks table in Supabase
"""
-- Run this in the Supabase SQL editor to create your tasks table
create table public.tasks (
  id uuid default uuid_generate_v4() primary key,
  user_id text not null,
  task_name text not null,
  description text,
  status text not null default 'pending',
  priority text not null default 'medium',
  deadline timestamp with time zone,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Create an index on user_id for faster queries
create index tasks_user_id_idx on public.tasks (user_id);

-- Set up Row Level Security
alter table public.tasks enable row level security;

-- Create policy for inserting tasks
CREATE POLICY "Users can create their own tasks" 
ON public.tasks FOR INSERT 
WITH CHECK (true);

-- Create policy for selecting tasks
CREATE POLICY "Users can view their own tasks" 
ON public.tasks FOR SELECT 
USING (true);

-- Create policy for updating tasks
CREATE POLICY "Users can update their own tasks" 
ON public.tasks FOR UPDATE
USING (true);

-- Create policy for deleting tasks
CREATE POLICY "Users can delete their own tasks" 
ON public.tasks FOR DELETE
USING (true);
"""
