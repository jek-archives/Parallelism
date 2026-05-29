CREATE TABLE IF NOT EXISTS votes (
    id          TEXT    PRIMARY KEY,

    user_id     TEXT    NOT NULL,
    poll_id     TEXT    NOT NULL,
    choice      TEXT    NOT NULL,
    edge_id     TEXT    NOT NULL,

    timestamp   FLOAT   NOT NULL,

    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

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

CREATE INDEX IF NOT EXISTS idx_votes_poll_id  ON votes(poll_id);
CREATE INDEX IF NOT EXISTS idx_votes_edge_id  ON votes(edge_id);
CREATE INDEX IF NOT EXISTS idx_votes_user_id  ON votes(user_id);
