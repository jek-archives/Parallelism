-- ─────────────────────────────────────────────────────────────────────────────
-- supabase_schema.sql
-- Run this in your Supabase project → SQL Editor to create the votes table.
-- ─────────────────────────────────────────────────────────────────────────────

-- Drop table if re-creating from scratch
-- DROP TABLE IF EXISTS votes;

CREATE TABLE IF NOT EXISTS votes (
    -- Composite idempotency key: one row per (user, poll) pair
    id          TEXT    PRIMARY KEY,         -- "{user_id}_{poll_id}"

    user_id     TEXT    NOT NULL,
    poll_id     TEXT    NOT NULL,
    choice      TEXT    NOT NULL,
    edge_id     TEXT    NOT NULL,

    -- Unix epoch float sent by the edge node; used to compute end-to-end latency
    timestamp   FLOAT   NOT NULL,

    -- Server-side audit columns (auto-managed by Postgres)
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Automatically update `updated_at` on every row change
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS votes_updated_at ON votes;
CREATE TRIGGER votes_updated_at
    BEFORE UPDATE ON votes
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Optional: helpful indexes
CREATE INDEX IF NOT EXISTS idx_votes_poll_id  ON votes(poll_id);
CREATE INDEX IF NOT EXISTS idx_votes_edge_id  ON votes(edge_id);
CREATE INDEX IF NOT EXISTS idx_votes_user_id  ON votes(user_id);

-- ── Verify the schema ────────────────────────────────────────────────────────
-- SELECT column_name, data_type FROM information_schema.columns
-- WHERE table_name = 'votes';
