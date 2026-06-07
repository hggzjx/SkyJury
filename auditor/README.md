# SkyJury Auditor

This directory contains the robustness-auditing pipeline for SkyJury:

- `build_llm_rubric_perturbations.py`: build length and language rubric reformulations
- `build_category_subset.py`: create category-balanced auditor subsets
- `audit_cross_candidate_perturbations.py`: compute confidence-shift robustness reports
- `audit_stats.py`: paired tests and multiple-testing utilities

For installation, data format, and portable run examples, see the top-level documentation:

- [../README.md](../README.md)

The shell scripts in this directory are batch-experiment wrappers. They may contain local model paths from the original experiment environment, so use the Python commands in the top-level README as the portable starting point.
