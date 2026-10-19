-- A diary can be rewritten on the same day; collection history must survive it.
CREATE TABLE IF NOT EXISTS public.yokai_collection (
    user_id VARCHAR(80) NOT NULL,
    collection_month DATE NOT NULL,
    yokai_id VARCHAR NOT NULL REFERENCES public.yokai_compendium(id),
    first_collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source VARCHAR(16) NOT NULL DEFAULT 'diary',
    PRIMARY KEY (user_id, collection_month, yokai_id)
);

ALTER TABLE public.yokai_collection ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.yokai_collection FROM anon, authenticated;

INSERT INTO public.yokai_collection (user_id, collection_month, yokai_id, source)
SELECT DISTINCT user_id, date_trunc('month', diary_date)::date, matched_yokai_id, 'diary'
FROM public.emotion_diary
WHERE matched_yokai_id IS NOT NULL
ON CONFLICT DO NOTHING;
