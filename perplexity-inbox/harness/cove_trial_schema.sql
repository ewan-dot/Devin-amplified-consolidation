-- cove_trial_schema.sql
-- Relational/Vector Schema V1 (Trial Sandbox on Cove database)
-- Configured for 384 dimensions to match local watcher model (all-MiniLM-L6-v2)

BEGIN;

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------------------------------------------------------------------
-- Shared enums
-- ---------------------------------------------------------------------

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'processing_status') THEN
    CREATE TYPE processing_status AS ENUM (
      'raw',
      'validated',
      'rejected',
      'indexed',
      'answered',
      'failed'
    );
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sovereign_mode') THEN
    CREATE TYPE sovereign_mode AS ENUM (
      'connected',
      'sovereign',
      'air_gapped'
    );
  END IF;
END $$;

-- ---------------------------------------------------------------------
-- 1. Raw Ingestion Ledger
-- ---------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS raw_ingestion_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  source_system TEXT NOT NULL,
  source_type TEXT NOT NULL,
  source_identifier TEXT,
  tenant_id TEXT NOT NULL DEFAULT 'internal',
  actor_identifier TEXT,
  raw_text TEXT,
  raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  raw_file_path TEXT,
  sha256 TEXT NOT NULL,
  status processing_status NOT NULL DEFAULT 'raw',
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_raw_ingestion_sha256
  ON raw_ingestion_log (tenant_id, sha256);

CREATE INDEX IF NOT EXISTS idx_raw_ingestion_received_at
  ON raw_ingestion_log (tenant_id, received_at DESC);

-- ---------------------------------------------------------------------
-- 2. Knowledge Nodes (384-dimensional pgvector)
-- ---------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS knowledge_nodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL DEFAULT 'internal',
  raw_ingestion_id UUID REFERENCES raw_ingestion_log(id) ON DELETE SET NULL,
  node_type TEXT NOT NULL,
  title TEXT,
  body TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  source_system TEXT,
  source_identifier TEXT,
  source_path TEXT,
  sha256 TEXT NOT NULL,

  -- PUDDING structural label: WHAT.HOW.SCALE.TIME
  label_what CHAR(1),
  label_how CHAR(1),
  label_scale CHAR(1),
  label_time TEXT,
  pudding_label TEXT GENERATED ALWAYS AS (
    label_what || '.' || label_how || '.' || label_scale || '.' || label_time
  ) STORED,

  semantic_dimensions TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
  epistemic_tag TEXT NOT NULL DEFAULT 'raw',
  provenance_weight NUMERIC(6,4) NOT NULL DEFAULT 1.0000,
  confidence NUMERIC(6,4),

  -- 384 dimensions for the local all-MiniLM-L6-v2 model
  embedding vector(384),

  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_knowledge_nodes_sha256
  ON knowledge_nodes (tenant_id, sha256, node_type);

CREATE INDEX IF NOT EXISTS idx_knowledge_nodes_type
  ON knowledge_nodes (tenant_id, node_type);

CREATE INDEX IF NOT EXISTS idx_knowledge_nodes_pudding_label
  ON knowledge_nodes (tenant_id, pudding_label);

-- ---------------------------------------------------------------------
-- 3. Markov Transitions
-- ---------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS knowledge_transitions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL DEFAULT 'internal',
  from_node_id UUID NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  to_node_id UUID NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
  transition_type TEXT NOT NULL DEFAULT 'observed',
  probability NUMERIC(10,8) NOT NULL CHECK (probability >= 0 AND probability <= 1),
  transition_count BIGINT NOT NULL DEFAULT 1,
  evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
  last_updated TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, from_node_id, to_node_id, transition_type)
);

-- ---------------------------------------------------------------------
-- 4. Sidecar Sessions
-- ---------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS sidecar_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL DEFAULT 'internal',
  channel TEXT NOT NULL,
  external_session_id TEXT,
  actor_identifier TEXT NOT NULL,
  mode sovereign_mode NOT NULL DEFAULT 'connected',
  sovereign_mode_active BOOLEAN NOT NULL DEFAULT false,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  ended_at TIMESTAMPTZ,
  context JSONB NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (tenant_id, channel, external_session_id)
);

-- ---------------------------------------------------------------------
-- 5. Agent Decisions
-- ---------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS agent_decisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL DEFAULT 'internal',
  session_id UUID REFERENCES sidecar_sessions(id) ON DELETE SET NULL,
  raw_ingestion_id UUID REFERENCES raw_ingestion_log(id) ON DELETE SET NULL,
  agent_name TEXT NOT NULL,
  model_name TEXT,
  decision_type TEXT NOT NULL,
  prompt_hash TEXT,
  input_summary TEXT,
  output_text TEXT,
  output_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  cited_node_ids UUID[] NOT NULL DEFAULT ARRAY[]::UUID[],
  confidence NUMERIC(6,4),
  quality_score NUMERIC(6,4),
  approved BOOLEAN NOT NULL DEFAULT false,
  escalated BOOLEAN NOT NULL DEFAULT false,
  escalation_reason TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------
-- 6. Retrieval Audit
-- ---------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS retrieval_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL DEFAULT 'internal',
  session_id UUID REFERENCES sidecar_sessions(id) ON DELETE SET NULL,
  query_text TEXT NOT NULL,
  query_embedding vector(384),
  kolmogorov_filter JSONB NOT NULL DEFAULT '{}'::jsonb,
  pgvector_candidates JSONB NOT NULL DEFAULT '[]'::jsonb,
  wasserstein_rerank JSONB NOT NULL DEFAULT '[]'::jsonb,
  markov_augmentation JSONB NOT NULL DEFAULT '[]'::jsonb,
  pontryagin_stop JSONB NOT NULL DEFAULT '{}'::jsonb,
  accepted_node_ids UUID[] NOT NULL DEFAULT ARRAY[]::UUID[],
  latency_ms INTEGER,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------
-- 7. Utility Functions
-- ---------------------------------------------------------------------

CREATE OR REPLACE FUNCTION touch_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_knowledge_nodes_updated_at ON knowledge_nodes;
CREATE TRIGGER trg_knowledge_nodes_updated_at
BEFORE UPDATE ON knowledge_nodes
FOR EACH ROW
EXECUTE FUNCTION touch_updated_at();

COMMIT;
