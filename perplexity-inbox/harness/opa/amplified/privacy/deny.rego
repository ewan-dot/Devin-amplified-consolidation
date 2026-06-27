package amplified.privacy
import rego.v1

deny contains msg if {
    some value in input.emitted_values
    value.contains_pii == true
    not value.pii_minimised
    msg := sprintf("P0 (privacy): %v contains_pii without pii_minimised", [value.id])
}
