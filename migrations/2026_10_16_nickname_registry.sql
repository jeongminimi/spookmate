-- One small row per browser installation that completes the nickname contract.
-- This is a visit registry, not proof of a person's identity.
CREATE TABLE IF NOT EXISTS public.nickname_registry (
    client_id UUID PRIMARY KEY,
    nickname VARCHAR(12) NOT NULL,
    contract_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- The application backend reads this table through its server-side DB connection.
-- Browser clients must not read it through the Supabase Data API.
ALTER TABLE public.nickname_registry ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.nickname_registry FROM anon, authenticated;

CREATE INDEX IF NOT EXISTS nickname_registry_created_at_idx
    ON public.nickname_registry (created_at DESC);
