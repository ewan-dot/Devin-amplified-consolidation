package amplified.attribution
import rego.v1

_human := {"ewan", "architect", "human"}

deny contains msg if {
    some value in input.emitted_values
    value.claim
    not value.author
    msg := sprintf("P0 (attribution): %v missing author", [value.id])
}

deny contains msg if {
    some value in input.emitted_values
    value.emitter_class == "agent"
    lower(value.author) in _human
    not value.proxy_act
    msg := sprintf("P0 (attribution): agent %v credited human without proxy_act", [value.id])
}
