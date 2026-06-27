package amplified.winwin
import rego.v1

# Win-win = the AI gate. No one gets hurt.
# Agent tiered emissions must explicitly clear the harm gate.

deny contains msg if {
    some value in input.emitted_values
    value.emitter_class == "agent"
    value.claim
    not value.win_win_clear
    msg := sprintf("P0 (win-win): agent %v — no one gets hurt gate not cleared (win_win_clear)", [value.id])
}

deny contains msg if {
    some value in input.emitted_values
    value.harm_declared == true
    not value.no_one_hurt
    msg := sprintf("P0 (win-win): %v harm_declared without no_one_hurt", [value.id])
}
