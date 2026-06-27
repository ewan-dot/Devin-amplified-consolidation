package amplified.transparency
import rego.v1

_tier_order := {"INTUITED": 1, "STRUCTURED": 2, "MEASURED": 3, "PROVEN": 4}

_has_refs(value) if {
    count(value.source_refs) > 0
}

_has_refs(value) if {
    count(value.evidence_refs) > 0
}

deny contains msg if {
    some value in input.emitted_values
    value.claim
    not value.origin_type
    msg := sprintf("P0 (transparency): %v missing origin_type", [value.id])
}

deny contains msg if {
    some value in input.emitted_values
    _tier_order[value.claim] >= 2
    not _has_refs(value)
    msg := sprintf("P0 (transparency): %v STRUCTURED+ without source_refs/evidence_refs", [value.id])
}

deny contains msg if {
    some value in input.emitted_values
    value.attribution_stripped == true
    not value.laundering_witness_id
    msg := sprintf("P0 (transparency): %v stripped attribution without laundering_witness_id", [value.id])
}
