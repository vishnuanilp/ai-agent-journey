-- events table: schema changes made during week 10.
-- NOTE: the table itself and its original columns were created
-- by clicking in the Supabase dashboard and are NOT recorded here.
-- History starts from this point.

-- 2026-08-06  sat_ingest: arrival time supplied by the ingest page.
-- Deliberately no default and no not-null: the page supplies this
-- value, and rows created before this column existed keep NULL.
alter table public.events add column received_at timestamptz;