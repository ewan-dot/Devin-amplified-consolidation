package amplified.sovereignty
import rego.v1

deny contains msg if {
    some value in input.emitted_values
    value.path_ok == false
    msg := sprintf("P0 (sovereignty): %v outside allowed estate path", [value.id])
}

_tier_order := {"INTUITED": 1, "STRUCTURED": 2, "MEASURED": 3, "PROVEN": 4}

deny contains msg if {
    some value in input.emitted_values
    _tier_order[value.claim] >= 3
    not value.system_of_record
    msg := sprintf("P0 (sovereignty): %v MEASURED+ without system_of_record", [value.id])
}
