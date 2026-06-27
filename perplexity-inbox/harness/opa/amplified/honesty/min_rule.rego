package amplified.honesty
import rego.v1

# Tier ordering — Gödel t-norm operates on integers
_tier_order := {"INTUITED": 1, "STRUCTURED": 2, "MEASURED": 3, "PROVEN": 4}
_tier_name   := {1: "INTUITED", 2: "STRUCTURED", 3: "MEASURED", 4: "PROVEN"}

_human_authors := {"ewan", "architect", "human"}

# --- actor classification (human + agent, same shape rules) ---

actor_class(value) := cls if {
    value.emitter_class
    cls := value.emitter_class
} else := cls if {
    lower(value.author) in _human_authors
    cls := "human"
} else := cls if {
    value.author
    cls := "agent"
} else := "unknown"

_has_promotion(value) if {
    value.promotion_record_id
    value.promotion_record_id != ""
}

# --- effective tier (min-rule) ---

_claim_num(value) := n if {
    n := _tier_order[value.claim]
}

_input_floor(value) := f if {
    nums := {_tier_order[t] | some t in value.input_tiers}
    count(nums) > 0
    f := min(nums)
} else := 4

_precond_floor(value) := _tier_order[value.precondition_floor] if {
    value.precondition_floor
} else := 4

_llm_floor(value) := 1 if {
    value.consulted_llm_at_runtime == true
} else := 4

effective_tier(value) := name if {
    num := min({
        _claim_num(value),
        _input_floor(value),
        _precond_floor(value),
        _llm_floor(value),
    })
    name := _tier_name[num]
}

# --- deny rules (shape only — not semantic truth) ---

# P0: layer claims more than min-rule permits
deny contains msg if {
    some value in input.emitted_values
    claimed  := _tier_order[value.claim]
    eff_name := effective_tier(value)
    effective := _tier_order[eff_name]
    claimed > effective
    msg := sprintf("P0 (shape §3): %v claims %v, min-rule permits %v", [value.id, value.claim, eff_name])
}

# P0: bare value (no claim) crossing boundary
deny contains msg if {
    some value in input.emitted_values
    not value.claim
    msg := sprintf("P0 (shape §2): bare value %v crossed boundary without tier", [value.id])
}

# P0: unknown tier string
deny contains msg if {
    some value in input.emitted_values
    value.claim
    not _tier_order[value.claim]
    msg := sprintf("P0 (shape §2): %v has unknown tier %v", [value.id, value.claim])
}

# P0: LLM consulted at runtime but claim above INTUITED
deny contains msg if {
    some value in input.emitted_values
    value.consulted_llm_at_runtime == true
    _tier_order[value.claim] > 1
    msg := sprintf("P0 (shape §4): %v consulted LLM at runtime, capped at INTUITED, claimed %v", [value.id, value.claim])
}

# P0: tiered boundary without author (attribution + honesty shape)
deny contains msg if {
    some value in input.emitted_values
    value.claim
    not value.author
    msg := sprintf("P0 (shape §5): %v crossed tiered boundary without author", [value.id])
}

# P0: agent seat attributed human author without proxy_act
deny contains msg if {
    some value in input.emitted_values
    value.emitter_class == "agent"
    lower(value.author) in _human_authors
    not value.proxy_act
    msg := sprintf("P0 (shape §6): agent emission %v used human author without proxy_act", [value.id])
}

# P0: self-ceiling without promotion (human seat)
deny contains msg if {
    some value in input.emitted_values
    value.emitter_class == "human"
    not _has_promotion(value)
    _tier_order[value.claim] > 1
    msg := sprintf("P0 (shape §7): human emission %v claims %v; default INTUITED until promotion_record_id", [value.id, value.claim])
}

# P0: self-ceiling without promotion (agent seat)
deny contains msg if {
    some value in input.emitted_values
    value.emitter_class == "agent"
    not _has_promotion(value)
    _tier_order[value.claim] > 1
    msg := sprintf("P0 (shape §8): agent emission %v claims %v; self-ceiling INTUITED without promotion_record_id", [value.id, value.claim])
}
