package amplified.security
import rego.v1

# Security — protect ourselves and our clients.

deny contains msg if {
    some value in input.emitted_values
    value.has_secret_in_metadata == true
    msg := sprintf("P0 (security): %v frontmatter matches secret shape", [value.id])
}

deny contains msg if {
    some value in input.emitted_values
    value.client_scope == true
    not value.client_consent
    msg := sprintf("P0 (security): %v client_scope without client_consent", [value.id])
}
