package amplified.boundary
import rego.v1

# One bee — all rods + PSS shape denies
deny contains msg if { some m in data.amplified.honesty.deny; msg := m }
deny contains msg if { some m in data.amplified.transparency.deny; msg := m }
deny contains msg if { some m in data.amplified.attribution.deny; msg := m }
deny contains msg if { some m in data.amplified.winwin.deny; msg := m }
deny contains msg if { some m in data.amplified.meritocracy.deny; msg := m }
deny contains msg if { some m in data.amplified.privacy.deny; msg := m }
deny contains msg if { some m in data.amplified.security.deny; msg := m }
deny contains msg if { some m in data.amplified.sovereignty.deny; msg := m }
