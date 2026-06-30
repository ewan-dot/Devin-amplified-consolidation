#!/usr/bin/env python3
"""Test harness for glasses_loader, shape_gate integration, and swanson_pudding_curator.

Validates that schemas are gated correctly under the 17-20 fields limit,
checks value constraints, and tests the LBD curation scoring logic.
"""
import os
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

HARNESS_DIR = Path(__file__).resolve().parent
sys.path.append(str(HARNESS_DIR))

from glasses_loader import load_lens_glasses, load_registry
from shape_gate import check_content
from swanson_pudding_curator import calculate_scores, make_pudding_recipe


class TestGlassesAndPudding(unittest.TestCase):
    
    def setUp(self):
        self.registry = load_registry()

    def test_valid_pudding_schema(self):
        # A valid PUDDING_V1 schema with exactly 20 fields
        valid_content = """---
schema_code: PUDDING_V1
id: TEST_PUDDING_01
title: "Dalio's Idea Meritocracy"
document_type: principle
expert: DALIO
domain: systems
semantic_dimensions:
  - cause_effect
  - trust
  - people
actionable: principle_only
status: canonical
pudding_score: 15
created_at: "2026-06-30"
last_validated: "2026-06-30"
lbd_attribution: "Swanson (1986) ABC Model"
epistemic_tier: INTUITED
provenance_sources: []
author: ewan
bridge_candidates: []
resolved_connections: []
risk_flags: []
canonical_summary: "A brief summary of Dalio's idea meritocracy."
---
Body text here.
"""
        res = load_lens_glasses(valid_content)
        self.assertEqual(res["status"], "VALID", f"Errors: {res.get('errors')}")
        self.assertEqual(res["schema_code"], "PUDDING_V1")
        self.assertIn("Swanson LBD", res["instructions"])

        # Run it through shape_gate check_content
        errors, fm = check_content(valid_content, "test.md", "human")
        self.assertEqual(len(errors), 0, f"Shape gate errors: {errors}")

    def test_invalid_field_count(self):
        # A schema with only 10 fields (violating the 17-20 limit)
        invalid_count_content = """---
schema_code: PUDDING_V1
id: TEST_PUDDING_02
title: "Short Field Count"
document_type: principle
expert: DALIO
domain: systems
semantic_dimensions:
  - cause_effect
actionable: principle_only
status: canonical
epistemic_tier: STRUCTURED
---
"""
        res = load_lens_glasses(invalid_count_content)
        self.assertEqual(res["status"], "INVALID")
        self.assertTrue(any("field count" in err for err in res["errors"]))

    def test_missing_required_field(self):
        # Missing required field 'expert' but has 18 fields total
        missing_field_content = """---
schema_code: PUDDING_V1
id: TEST_PUDDING_03
title: "Missing Expert"
document_type: principle
domain: systems
semantic_dimensions:
  - cause_effect
actionable: principle_only
status: canonical
pudding_score: 15
created_at: "2026-06-30"
last_validated: "2026-06-30"
lbd_attribution: "Swanson (1986) ABC Model"
epistemic_tier: STRUCTURED
provenance_sources: []
author: ewan
bridge_candidates: []
resolved_connections: []
risk_flags: []
canonical_summary: "Missing expert test case."
field1: dummy_val
---
"""
        res = load_lens_glasses(missing_field_content)
        self.assertEqual(res["status"], "INVALID")
        self.assertTrue(any("Missing required field: 'expert'" in err for err in res["errors"]))

    def test_invalid_enum_value(self):
        # Invalid epistemic_tier 'GUESSED'
        invalid_enum_content = """---
schema_code: PUDDING_V1
id: TEST_PUDDING_04
title: "Invalid Enum"
document_type: principle
expert: DALIO
domain: systems
semantic_dimensions:
  - cause_effect
actionable: principle_only
status: canonical
pudding_score: 15
created_at: "2026-06-30"
last_validated: "2026-06-30"
lbd_attribution: "Swanson (1986) ABC Model"
epistemic_tier: GUESSED
provenance_sources: []
author: ewan
bridge_candidates: []
resolved_connections: []
risk_flags: []
canonical_summary: "Invalid epistemic_tier enum test."
---
"""
        res = load_lens_glasses(invalid_enum_content)
        self.assertEqual(res["status"], "INVALID")
        self.assertTrue(any("Invalid value 'GUESSED' for field 'epistemic_tier'" in err for err in res["errors"]))

    def test_swanson_scoring_maths(self):
        # Item A: Gerber's E-Myth Systems (Gerber, domain: systems, dimensions: systems, cause_effect)
        a = {
            "id": "A_GERBER_01",
            "title": "Gerber Systems",
            "expert": "GERBER",
            "domain": "systems",
            "semantic_dimensions": ["systems", "cause_effect", "trust"]
        }
        # Item C: Kennedy's Direct Response Sales (Kennedy, domain: sales, dimensions: trust, feedback_loop)
        c = {
            "id": "C_KENNEDY_01",
            "title": "Kennedy Sales",
            "expert": "KENNEDY",
            "domain": "sales",
            "semantic_dimensions": ["trust", "feedback_loop", "pricing"]
        }

        # Calculate matching scores
        score_res = calculate_scores(a, c)

        # 1. Bridge B should be 'trust'
        self.assertIn("trust", score_res["shared"])
        self.assertEqual(len(score_res["shared"]), 1)

        # 2. Simple Recipe Score (F5): 2 * 1 (Shared) + 2 (Unique A) + 2 (Unique C) = 6
        self.assertEqual(score_res["e_simple"], 6)

        # 3. Jaccard Set (F4): 1 (Shared) / 5 (Union: systems, cause_effect, trust, feedback_loop, pricing) = 0.20
        self.assertAlmostEqual(score_res["j_set"], 0.20)

        # 4. Jaccard Slot (F3): 1 / 4 = 0.25
        self.assertEqual(score_res["j_slot"], 0.25)

        # 5. Pattern Alignment (F8): round(0.25 * 10) = 3
        self.assertEqual(score_res["pattern_align"], 3)

        # 6. Domain Distance: different expert AND different domain => 6
        self.assertEqual(score_res["domain_dist"], 6)

        # 7. Candidate Score (F7): (6 * 3) + 4 (GapComp: min(5, 2+2)) + 3 (TensionBonus) = 18 + 4 + 3 = 25
        self.assertEqual(score_res["s_candidate"], 25)

        # Test recipe frontmatter formatting
        recipe = make_pudding_recipe(a, c, score_res)
        self.assertIn("schema_code: PUDDING_V1", recipe)
        self.assertIn("pudding_score: 25", recipe)
        self.assertIn("RECIPE_HYPOTHESIS_", recipe)


if __name__ == "__main__":
    unittest.main()
