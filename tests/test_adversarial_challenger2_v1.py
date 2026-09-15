#!/usr/bin/env python3
"""
Adversarial Verification Suite - Challenger 2 (v1)
AutoExpert 20-Variant Pack

Checks:
1. Preamble Example Semantics & Realism (realistic, valid, non-placeholder across all 20 files)
2. Domain-Authentic Rules & Epilogues (non-technical domains replacing CODING RULES & EPILOGUE)
3. README.txt Consistency (accurate filename references, 0 missing, 0 typos, no forbidden formatting)
4. Adversarial Edge Cases (BOMs, control characters, CRLF vs LF, tabs, whitespace, word count stress tests)
"""

import os
import re
import sys
from pathlib import Path
import pytest

VARIANTS_DIR = Path("/Users/dad/Downloads/AutoExpert-Pack/variants")
README_FILE = VARIANTS_DIR / "README.txt"

EXPECTED_FILES = [
    "general_qa.txt",
    "software_engineering.txt",
    "data_analysis.txt",
    "research.txt",
    "legal.txt",
    "medical.txt",
    "hr_benefits.txt",
    "corporate_comms.txt",
    "creative_writing.txt",
    "finance.txt",
    "project_management.txt",
    "devops.txt",
    "cybersecurity.txt",
    "education.txt",
    "product_management.txt",
    "ux_design.txt",
    "sales.txt",
    "lab_notebook.txt",
    "parenting.txt",
    "municipal_gov.txt",
]

NON_TECHNICAL_DOMAINS = [
    "general_qa.txt",
    "data_analysis.txt",
    "research.txt",
    "legal.txt",
    "medical.txt",
    "hr_benefits.txt",
    "corporate_comms.txt",
    "creative_writing.txt",
    "finance.txt",
    "project_management.txt",
    "education.txt",
    "product_management.txt",
    "ux_design.txt",
    "sales.txt",
    "lab_notebook.txt",
    "parenting.txt",
    "municipal_gov.txt",
]

TECHNICAL_DOMAINS = [
    "software_engineering.txt",
    "devops.txt",
    "cybersecurity.txt",
]

FORBIDDEN_WORDS_REGEX = re.compile(r"\b(dossier|stack|seat)s?\b", re.IGNORECASE)

class AdversarialReport:
    def __init__(self):
        self.findings = []
        self.passes = []
        self.failures = []

    def record_pass(self, test_name, detail=""):
        self.passes.append((test_name, detail))

    def record_fail(self, test_name, reason, severity="HIGH"):
        self.failures.append((test_name, reason, severity))
        self.findings.append(f"[{severity}] {test_name}: {reason}")


def check_file_inventory(report):
    actual_files = set(f.name for f in VARIANTS_DIR.glob("*.txt"))
    expected_set = set(EXPECTED_FILES) | {"README.txt"}
    
    missing = expected_set - actual_files
    if missing:
        report.record_fail("File Inventory", f"Missing expected files: {sorted(missing)}", "CRITICAL")
    else:
        report.record_pass("File Inventory", f"All 20 variant files + README.txt present ({len(actual_files)} total files)")

    unexpected = actual_files - expected_set
    if unexpected:
        report.record_fail("File Inventory", f"Unexpected files found: {sorted(unexpected)}", "LOW")
    else:
        report.record_pass("File Inventory", "Zero unexpected files")


def check_word_counts(report):
    for fname in EXPECTED_FILES:
        fpath = VARIANTS_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        
        words = text.split()
        wc = len(words)
        re_words = re.findall(r"\S+", text)
        re_wc = len(re_words)
        
        if wc >= 500:
            report.record_fail(f"Word Count ({fname})", f"Exceeds 500 words: {wc} words", "CRITICAL")
        elif wc == 0:
            report.record_fail(f"Word Count ({fname})", "File is empty", "CRITICAL")
        else:
            report.record_pass(f"Word Count ({fname})", f"{wc} words (re_wc: {re_wc}, within < 500 limit)")


def check_forbidden_chars_and_terms(report):
    for fname in EXPECTED_FILES + ["README.txt"]:
        fpath = VARIANTS_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        
        if "#" in text:
            lines = text.splitlines()
            for idx, line in enumerate(lines, 1):
                if "#" in line:
                    report.record_fail(f"Forbidden Character '#' ({fname})", f"Found '#' on line {idx}: {line.strip()}", "CRITICAL")
        else:
            report.record_pass(f"Forbidden Character '#' ({fname})", "0 '#' occurrences")

        if "**" in text:
            lines = text.splitlines()
            for idx, line in enumerate(lines, 1):
                if "**" in line:
                    report.record_fail(f"Forbidden Character '**' ({fname})", f"Found '**' on line {idx}: {line.strip()}", "CRITICAL")
        else:
            report.record_pass(f"Forbidden Character '**' ({fname})", "0 '**' occurrences")

        matches = list(FORBIDDEN_WORDS_REGEX.finditer(text))
        if matches:
            for m in matches:
                report.record_fail(f"Forbidden Vocabulary ({fname})", f"Found forbidden term '{m.group()}' at pos {m.start()}", "HIGH")
        else:
            report.record_pass(f"Forbidden Vocabulary ({fname})", "0 forbidden vocabulary terms")


def check_preamble_examples(report):
    for fname in EXPECTED_FILES:
        fpath = VARIANTS_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")

        step1_idx = text.find("STEP 1")
        step2_idx = text.find("STEP 2")

        if step1_idx == -1 or step2_idx == -1:
            report.record_fail(f"Preamble Structure ({fname})", "Missing STEP 1 or STEP 2 marker", "CRITICAL")
            continue

        step1_section = text[step1_idx:step2_idx]

        ex_match = re.search(r"Example[^\n]*\n", step1_section, re.IGNORECASE)
        if not ex_match:
            report.record_fail(f"Preamble Example ({fname})", "No 'Example' header found in STEP 1", "CRITICAL")
            continue

        example_part = step1_section[ex_match.end():]

        expert_match = re.search(r"Expert:\s*([^\n]+)", example_part)
        v_match = re.search(r"V:\s*([^\n]+)", example_part)
        goal_match = re.search(r"Goal:\s*([^\n]+)", example_part)
        plan_match = re.search(r"Plan:\s*([^\n]+(?:\n\s*[0-9]\.[^\n]+)*)", example_part)

        if not expert_match:
            report.record_fail(f"Preamble Example Expert ({fname})", "Missing 'Expert:' in example", "CRITICAL")
        else:
            expert_val = expert_match.group(1).strip()
            if "[" in expert_val or "]" in expert_val:
                report.record_fail(f"Preamble Example Expert ({fname})", f"Placeholder brackets in expert: '{expert_val}'", "HIGH")
            elif "helpful assistant" in expert_val.lower():
                report.record_fail(f"Preamble Example Expert ({fname})", f"Generic assistant in expert: '{expert_val}'", "HIGH")
            elif len(expert_val) < 8:
                report.record_fail(f"Preamble Example Expert ({fname})", f"Too short expert persona: '{expert_val}'", "HIGH")
            else:
                report.record_pass(f"Preamble Example Expert ({fname})", f"Valid persona: '{expert_val}'")

        if not v_match:
            report.record_fail(f"Preamble Example V ({fname})", "Missing 'V:' in example", "CRITICAL")
        else:
            v_val = v_match.group(1).strip()
            if "[" in v_val or "]" in v_val:
                report.record_fail(f"Preamble Example V ({fname})", f"Placeholder brackets in V: '{v_val}'", "HIGH")
            else:
                report.record_pass(f"Preamble Example V ({fname})", f"Valid V setting: '{v_val}'")

        if not goal_match:
            report.record_fail(f"Preamble Example Goal ({fname})", "Missing 'Goal:' in example", "CRITICAL")
        else:
            goal_val = goal_match.group(1).strip()
            if "[" in goal_val or "]" in goal_val:
                report.record_fail(f"Preamble Example Goal ({fname})", f"Placeholder brackets in goal: '{goal_val}'", "HIGH")
            elif len(goal_val) < 15:
                report.record_fail(f"Preamble Example Goal ({fname})", f"Too short/trivial goal: '{goal_val}'", "HIGH")
            else:
                report.record_pass(f"Preamble Example Goal ({fname})", f"Valid goal: '{goal_val}'")

        if not plan_match:
            report.record_fail(f"Preamble Example Plan ({fname})", "Missing 'Plan:' in example", "CRITICAL")
        else:
            plan_val = plan_match.group(1).strip()
            if "[" in plan_val or "]" in plan_val:
                report.record_fail(f"Preamble Example Plan ({fname})", f"Placeholder brackets in plan: '{plan_val}'", "HIGH")
            elif "1." not in plan_val:
                report.record_fail(f"Preamble Example Plan ({fname})", f"Plan lacks numbered step '1.': '{plan_val}'", "HIGH")
            else:
                report.record_pass(f"Preamble Example Plan ({fname})", f"Valid plan steps: '{plan_val}'")

        bracket_matches = re.findall(r"\[.*?\]", example_part)
        if bracket_matches:
            report.record_fail(f"Preamble Example Bracket Check ({fname})", f"Found unresolved bracketed placeholders in example: {bracket_matches}", "HIGH")
        else:
            report.record_pass(f"Preamble Example Bracket Check ({fname})", "0 unresolved placeholder brackets")


def check_domain_rules_and_epilogues(report):
    for fname in EXPECTED_FILES:
        fpath = VARIANTS_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")

        is_non_technical = fname in NON_TECHNICAL_DOMAINS

        rules_match = re.search(r"\n([A-Z0-9\s&/\-_]+RULES):", text)
        epilogue_match = re.search(r"\n([A-Z0-9\s&/\-_]+EPILOGUE(?:\s*\([^)]*\))?):", text)

        if is_non_technical:
            if "CODING RULES" in text:
                report.record_fail(f"Domain Rules ({fname})", "Retains literal 'CODING RULES' in non-technical domain", "CRITICAL")
            elif rules_match:
                report.record_pass(f"Domain Rules ({fname})", f"Adapted: '{rules_match.group(1).strip()}'")
            else:
                report.record_fail(f"Domain Rules ({fname})", "Could not find adapted *RULES: section", "HIGH")

            if "CODING EPILOGUE" in text:
                report.record_fail(f"Domain Epilogue ({fname})", "Retains literal 'CODING EPILOGUE' in non-technical domain", "CRITICAL")
            elif epilogue_match:
                report.record_pass(f"Domain Epilogue ({fname})", f"Adapted: '{epilogue_match.group(1).strip()}'")
            else:
                report.record_fail(f"Domain Epilogue ({fname})", "Could not find adapted *EPILOGUE: section", "HIGH")

            if "tested symbol()" in text or "blocked symbol()" in text:
                report.record_fail(f"Domain Epilogue Ledger ({fname})", "Retains coding-specific symbols ('tested symbol()')", "HIGH")
            elif "saved file.ext" in text and fname != "data_analysis.txt":
                report.record_fail(f"Domain Epilogue Ledger ({fname})", "Retains generic coding 'saved file.ext'", "MEDIUM")
            else:
                report.record_pass(f"Domain Epilogue Ledger ({fname})", "Domain-authentic ledger items")

        else:
            if rules_match:
                report.record_pass(f"Technical Rules ({fname})", f"Rules present: '{rules_match.group(1).strip()}'")
            else:
                report.record_fail(f"Technical Rules ({fname})", "Missing RULES section", "HIGH")

            if epilogue_match:
                report.record_pass(f"Technical Epilogue ({fname})", f"Epilogue present: '{epilogue_match.group(1).strip()}'")
            else:
                report.record_fail(f"Technical Epilogue ({fname})", "Missing EPILOGUE section", "HIGH")


def check_readme_consistency(report):
    if not README_FILE.exists():
        report.record_fail("README", "README.txt does not exist", "CRITICAL")
        return

    readme_text = README_FILE.read_text(encoding="utf-8")

    for fname in EXPECTED_FILES:
        if fname not in readme_text:
            report.record_fail("README File Reference", f"Expected variant '{fname}' not found in README.txt", "CRITICAL")
        else:
            report.record_pass(f"README File Reference ({fname})", "Found in README.txt")

    mentioned_txts = set(re.findall(r"\b([a-z0-9_]+\.txt)\b", readme_text))
    mentioned_variants = mentioned_txts - {"README.txt", "readme.txt"}

    phantom_files = mentioned_variants - set(EXPECTED_FILES)
    if phantom_files:
        report.record_fail("README Phantom Reference", f"README mentions nonexistent files: {sorted(phantom_files)}", "HIGH")
    else:
        report.record_pass("README Phantom Reference", "Zero phantom file references in README.txt")

    catalog_match = re.search(r"COMPLETE CATALOG OF 20 DOMAIN VARIANTS", readme_text)
    if catalog_match:
        report.record_pass("README Catalog Header", "Catalog header found")
    else:
        report.record_fail("README Catalog Header", "Missing 'COMPLETE CATALOG OF 20 DOMAIN VARIANTS'", "HIGH")

    if "WHEN TO USE" not in readme_text and "DOMAIN SELECTION GUIDE" not in readme_text:
        report.record_fail("README Usage Guidance", "README missing domain selection guidance", "MEDIUM")
    else:
        report.record_pass("README Usage Guidance", "Domain selection guidance present")


def check_adversarial_edge_cases(report):
    for fname in EXPECTED_FILES + ["README.txt"]:
        fpath = VARIANTS_DIR / fname
        if not fpath.exists():
            continue

        raw_bytes = fpath.read_bytes()

        if raw_bytes.startswith(b"\xef\xbb\xbf"):
            report.record_fail(f"BOM ({fname})", "Contains UTF-8 Byte Order Mark (BOM)", "HIGH")
        elif raw_bytes.startswith(b"\xff\xfe") or raw_bytes.startswith(b"\xfe\xff"):
            report.record_fail(f"BOM ({fname})", "Contains UTF-16 BOM", "CRITICAL")
        elif raw_bytes.startswith(b"\x00\x00\xfe\xff") or raw_bytes.startswith(b"\xff\xfe\x00\x00"):
            report.record_fail(f"BOM ({fname})", "Contains UTF-32 BOM", "CRITICAL")
        else:
            report.record_pass(f"BOM ({fname})", "No BOM detected (clean start of file)")

        if b"\r\n" in raw_bytes:
            report.record_fail(f"Line Endings ({fname})", "Contains CRLF (Windows) line endings", "MEDIUM")
        elif b"\r" in raw_bytes:
            report.record_fail(f"Line Endings ({fname})", "Contains CR (Classic Mac) line endings", "MEDIUM")
        else:
            report.record_pass(f"Line Endings ({fname})", "Clean Unix LF (\\n) line endings")

        rogue_ctrl = []
        for idx, b in enumerate(raw_bytes):
            if b < 32 and b not in (9, 10):
                rogue_ctrl.append((idx, hex(b)))
        if rogue_ctrl:
            report.record_fail(f"Control Character ({fname})", f"Found rogue control bytes: {rogue_ctrl[:5]}", "HIGH")
        else:
            report.record_pass(f"Control Character ({fname})", "Zero rogue control characters")

        try:
            text = raw_bytes.decode("utf-8")
            report.record_pass(f"UTF-8 Encoding ({fname})", "Valid UTF-8")
        except UnicodeDecodeError as e:
            report.record_fail(f"UTF-8 Encoding ({fname})", f"UTF-8 decode failure: {e}", "CRITICAL")
            continue

        if "\t" in text:
            tab_count = text.count("\t")
            report.record_fail(f"Whitespace Normalization ({fname})", f"Contains {tab_count} raw TAB characters", "LOW")
        else:
            report.record_pass(f"Whitespace Normalization ({fname})", "Zero TAB characters (pure spaces)")

        if "\u00a0" in text:
            report.record_fail(f"Special Whitespace ({fname})", "Contains non-breaking space (U+00A0)", "LOW")
        else:
            report.record_pass(f"Special Whitespace ({fname})", "Zero non-breaking spaces")

        if "\u200b" in text:
            report.record_fail(f"Special Whitespace ({fname})", "Contains zero-width space (U+200B)", "HIGH")
        else:
            report.record_pass(f"Special Whitespace ({fname})", "Zero zero-width spaces")


def run_all_checks():
    report = AdversarialReport()
    check_file_inventory(report)
    check_word_counts(report)
    check_forbidden_chars_and_terms(report)
    check_preamble_examples(report)
    check_domain_rules_and_epilogues(report)
    check_readme_consistency(report)
    check_adversarial_edge_cases(report)

    print("\n" + "=" * 80)
    print("ADVERSARIAL VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Total Passes:   {len(report.passes)}")
    print(f"Total Failures: {len(report.failures)}")

    if report.failures:
        print("\nFAILURES DETECTED:")
        for name, reason, sev in report.failures:
            print(f"  [{sev}] {name}: {reason}")
        verdict = "REQUEST_CHANGES"
    else:
        print("\nALL ADVERSARIAL CHECKS PASSED EMPIRICALLY WITH ZERO DEFECTS!")
        verdict = "APPROVE"

    print("=" * 80)
    print(f"VERDICT: {verdict}")
    print("=" * 80)
    return verdict, report


# Pytest entry points
def test_adversarial_file_inventory():
    report = AdversarialReport()
    check_file_inventory(report)
    assert len(report.failures) == 0, f"Failures: {report.failures}"

def test_adversarial_word_counts():
    report = AdversarialReport()
    check_word_counts(report)
    assert len(report.failures) == 0, f"Failures: {report.failures}"

def test_adversarial_forbidden_chars_and_terms():
    report = AdversarialReport()
    check_forbidden_chars_and_terms(report)
    assert len(report.failures) == 0, f"Failures: {report.failures}"

def test_adversarial_preamble_examples():
    report = AdversarialReport()
    check_preamble_examples(report)
    assert len(report.failures) == 0, f"Failures: {report.failures}"

def test_adversarial_domain_rules_and_epilogues():
    report = AdversarialReport()
    check_domain_rules_and_epilogues(report)
    assert len(report.failures) == 0, f"Failures: {report.failures}"

def test_adversarial_readme_consistency():
    report = AdversarialReport()
    check_readme_consistency(report)
    assert len(report.failures) == 0, f"Failures: {report.failures}"

def test_adversarial_edge_cases():
    report = AdversarialReport()
    check_adversarial_edge_cases(report)
    assert len(report.failures) == 0, f"Failures: {report.failures}"


if __name__ == "__main__":
    verdict, report = run_all_checks()
    sys.exit(0 if verdict == "APPROVE" else 1)
