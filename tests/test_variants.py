#!/usr/bin/env python3
# <!-- v1 – Comprehensive 4-Tier Automated Test Suite for AutoExpert Variants Pack -->
"""
AutoExpert Variants Pack Automated E2E Test Suite.

Validates 20 domain-specific AI system prompt variants and README.txt
across 4 strict compliance tiers:
- Tier 1: File Existence & Basic Content
- Tier 2: Boundary & Formatting Invariants (Word Count < 500, Zero '#', Zero '**', Zero Forbidden Terms)
- Tier 3: Structural Lifecycle & Domain Customization (5-Step Lifecycle, Filled Preamble Example,
          Verbosity Scale, Domain Rules/Epilogue, Slash Commands, Footer Directive)
- Tier 4: Self-Contained Deployment & README Master Index

Supports both direct CLI execution and pytest runner.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Default directory for variant pack
DEFAULT_VARIANTS_DIR = Path("/Users/dad/Downloads/AutoExpert-Pack/variants")

# Inventory of all 20 expected variant files
VARIANT_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
    "general_qa.txt": {
        "index": 1,
        "batch": 1,
        "technical": False,
        "domain": "General Knowledge Q&A",
        "expected_role_keywords": ["polymath", "inquiry", "epistemologist"],
        "expected_rules_keyword": "EPISTEMIC",
        "expected_epilogue_keyword": "INQUIRY",
    },
    "software_engineering.txt": {
        "index": 2,
        "batch": 1,
        "technical": True,
        "domain": "Software Engineering / Pair Programming",
        "expected_role_keywords": ["software", "architect", "engineer", "programmer"],
        "expected_rules_keyword": "CODING",
        "expected_epilogue_keyword": "CODING",
    },
    "data_analysis.txt": {
        "index": 3,
        "batch": 1,
        "technical": False,
        "domain": "Data Analysis & Statistics",
        "expected_role_keywords": ["data", "statistician", "scientist", "quantitative"],
        "expected_rules_keyword": "DATA",
        "expected_epilogue_keyword": "ANALYSIS",
    },
    "research.txt": {
        "index": 4,
        "batch": 1,
        "technical": False,
        "domain": "Research & Literature Review",
        "expected_role_keywords": ["research", "methodologist", "literature", "scientist"],
        "expected_rules_keyword": "CITATION",
        "expected_epilogue_keyword": "SYNTHESIS",
    },
    "legal.txt": {
        "index": 5,
        "batch": 1,
        "technical": False,
        "domain": "Legal Document Review & Compliance",
        "expected_role_keywords": ["legal", "counsel", "attorney", "regulatory"],
        "expected_rules_keyword": "JURISPRUDENTIAL",
        "expected_epilogue_keyword": "LEGAL",
    },
    "medical.txt": {
        "index": 6,
        "batch": 2,
        "technical": False,
        "domain": "Medical / Clinical Research",
        "expected_role_keywords": ["medical", "clinical", "pharmacologist", "physician"],
        "expected_rules_keyword": "CLINICAL",
        "expected_epilogue_keyword": "CLINICAL",
    },
    "hr_benefits.txt": {
        "index": 7,
        "batch": 2,
        "technical": False,
        "domain": "Benefits & HR Administration",
        "expected_role_keywords": ["people", "benefits", "human resources", "hr", "rewards"],
        "expected_rules_keyword": "BENEFITS",
        "expected_epilogue_keyword": "HR",
    },
    "corporate_comms.txt": {
        "index": 8,
        "batch": 2,
        "technical": False,
        "domain": "Corporate Communications & PR",
        "expected_role_keywords": ["communications", "pr", "media", "spokesperson"],
        "expected_rules_keyword": "MESSAGING",
        "expected_epilogue_keyword": "COMMUNICATIONS",
    },
    "creative_writing.txt": {
        "index": 9,
        "batch": 2,
        "technical": False,
        "domain": "Creative Writing & Copywriting",
        "expected_role_keywords": ["story", "writer", "editor", "narrative", "author"],
        "expected_rules_keyword": "NARRATIVE",
        "expected_epilogue_keyword": "MANUSCRIPT",
    },
    "finance.txt": {
        "index": 10,
        "batch": 2,
        "technical": False,
        "domain": "Financial Analysis & Accounting",
        "expected_role_keywords": ["financial", "finance", "cfo", "valuation", "analyst"],
        "expected_rules_keyword": "FINANCIAL",
        "expected_epilogue_keyword": "FINANCIAL",
    },
    "project_management.txt": {
        "index": 11,
        "batch": 3,
        "technical": False,
        "domain": "Project Management & Planning",
        "expected_role_keywords": ["project", "program", "agile", "operations", "scrum"],
        "expected_rules_keyword": "PROJECT",
        "expected_epilogue_keyword": "SPRINT",
    },
    "devops.txt": {
        "index": 12,
        "batch": 3,
        "technical": True,
        "domain": "DevOps & Infrastructure",
        "expected_role_keywords": ["sre", "devops", "cloud", "infrastructure", "reliability"],
        "expected_rules_keyword": "INFRASTRUCTURE",
        "expected_epilogue_keyword": "DEPLOYMENT",
    },
    "cybersecurity.txt": {
        "index": 13,
        "batch": 3,
        "technical": True,
        "domain": "Cybersecurity & Threat Analysis",
        "expected_role_keywords": ["security", "threat", "ciso", "cyber", "hunter"],
        "expected_rules_keyword": "SECURITY",
        "expected_epilogue_keyword": "REMEDIATION",
    },
    "education.txt": {
        "index": 14,
        "batch": 3,
        "technical": False,
        "domain": "Education & Tutoring",
        "expected_role_keywords": ["educator", "pedagogical", "teacher", "curriculum", "tutor"],
        "expected_rules_keyword": "PEDAGOGICAL",
        "expected_epilogue_keyword": "LEARNING",
    },
    "product_management.txt": {
        "index": 15,
        "batch": 3,
        "technical": False,
        "domain": "Product Management & Strategy",
        "expected_role_keywords": ["product", "strategy", "prd", "roadmap", "vp"],
        "expected_rules_keyword": "PRODUCT",
        "expected_epilogue_keyword": "PRODUCT",
    },
    "ux_design.txt": {
        "index": 16,
        "batch": 4,
        "technical": False,
        "domain": "UX/UI Design Critique",
        "expected_role_keywords": ["ux", "ui", "design", "interaction", "designer"],
        "expected_rules_keyword": "DESIGN",
        "expected_epilogue_keyword": "DESIGN",
    },
    "sales.txt": {
        "index": 17,
        "batch": 4,
        "technical": False,
        "domain": "Sales & Proposal Writing",
        "expected_role_keywords": ["sales", "revenue", "deal", "proposal", "account"],
        "expected_rules_keyword": "PROPOSAL",
        "expected_epilogue_keyword": "SALES",
    },
    "lab_notebook.txt": {
        "index": 18,
        "batch": 4,
        "technical": False,
        "domain": "Scientific Lab Notebook / Wet Lab",
        "expected_role_keywords": ["lab", "protocol", "scientist", "investigator", "assay"],
        "expected_rules_keyword": "EXPERIMENTAL",
        "expected_epilogue_keyword": "LAB",
    },
    "parenting.txt": {
        "index": 19,
        "batch": 4,
        "technical": False,
        "domain": "Parenting & Family Logistics",
        "expected_role_keywords": ["parenting", "family", "pediatric", "child", "developmental"],
        "expected_rules_keyword": "FAMILY",
        "expected_epilogue_keyword": "FAMILY",
    },
    "municipal_gov.txt": {
        "index": 20,
        "batch": 4,
        "technical": False,
        "domain": "Municipal Government & Public Records",
        "expected_role_keywords": ["municipal", "government", "civic", "city", "council"],
        "expected_rules_keyword": "GOVERNANCE",
        "expected_epilogue_keyword": "DOCKET",
    },
}

ALL_VARIANT_FILES = list(VARIANT_SPECIFICATIONS.keys())
README_FILE = "README.txt"
ALL_PACK_FILES = ALL_VARIANT_FILES + [README_FILE]

# Universal slash commands that must appear in every variant
UNIVERSAL_COMMANDS = ["/help", "/v", "/review", "/summary"]

# Forbidden markdown characters
FORBIDDEN_CHARACTERS = ["#", "**"]

# Forbidden vocabulary pattern (user-defined global constraint)
FORBIDDEN_TERMS_PATTERN = re.compile(r"(?i)\b\w*(dossier|stack|seat)\w*\b")


@dataclass
class ValidationIssue:
    tier: int
    rule: str
    message: str
    severity: str = "ERROR"  # ERROR or WARNING


@dataclass
class FileValidationResult:
    filename: str
    exists: bool = False
    word_count: int = 0
    passed_tier1: bool = False
    passed_tier2: bool = False
    passed_tier3: bool = False
    passed_tier4: bool = False
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return all(issue.severity != "ERROR" for issue in self.issues)


class VariantPackValidator:
    """
    Automated validator executing 4-tier compliance checks against
    the AutoExpert domain variants pack.
    """

    def __init__(self, target_dir: Path):
        self.target_dir = Path(target_dir).expanduser().resolve()

    def get_file_content(self, filename: str) -> Optional[str]:
        filepath = self.target_dir / filename
        if not filepath.is_file():
            return None
        try:
            return filepath.read_text(encoding="utf-8")
        except Exception:
            return None

    def validate_variant_file(self, filename: str) -> FileValidationResult:
        result = FileValidationResult(filename=filename)
        spec = VARIANT_SPECIFICATIONS.get(filename)
        if not spec:
            result.issues.append(
                ValidationIssue(tier=1, rule="KnownVariant", message=f"Unrecognized variant filename: {filename}")
            )
            return result

        filepath = self.target_dir / filename

        # --- Tier 1: File Existence & Basic Content ---
        if not filepath.exists():
            result.issues.append(
                ValidationIssue(tier=1, rule="FileExistence", message=f"Variant file missing at {filepath}")
            )
            return result
        if not filepath.is_file():
            result.issues.append(
                ValidationIssue(tier=1, rule="FileExistence", message=f"Target path is not a regular file: {filepath}")
            )
            return result

        result.exists = True

        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as exc:
            result.issues.append(
                ValidationIssue(tier=1, rule="FileReadability", message=f"Failed to read file as UTF-8: {exc}")
            )
            return result

        if not content.strip():
            result.issues.append(
                ValidationIssue(tier=1, rule="FileNotEmpty", message=f"Variant file is empty: {filename}")
            )
            return result

        result.passed_tier1 = True

        # --- Tier 2: Boundary & Formatting Invariants ---
        words = content.split()
        result.word_count = len(words)

        # Word count check: strictly > 0 and < 500 words
        if not (0 < result.word_count < 500):
            result.issues.append(
                ValidationIssue(
                    tier=2,
                    rule="WordCountBounds",
                    message=f"Word count violation: {result.word_count} words (must be strictly > 0 and < 500 words)",
                )
            )

        # Character check: 0 occurrences of '#'
        if "#" in content:
            hash_count = content.count("#")
            result.issues.append(
                ValidationIssue(
                    tier=2,
                    rule="ZeroMarkdownHash",
                    message=f"Markdown forbidden character '#' detected ({hash_count} occurrence(s))",
                )
            )

        # Character check: 0 occurrences of '**'
        if "**" in content:
            bold_count = content.count("**")
            result.issues.append(
                ValidationIssue(
                    tier=2,
                    rule="ZeroMarkdownBold",
                    message=f"Markdown forbidden character '**' detected ({bold_count} occurrence(s))",
                )
            )

        # Forbidden terms check: zero occurrences of forbidden vocabulary
        forbidden_matches = FORBIDDEN_TERMS_PATTERN.findall(content)
        if forbidden_matches:
            result.issues.append(
                ValidationIssue(
                    tier=2,
                    rule="ZeroForbiddenTerms",
                    message=f"Forbidden vocabulary detected ({len(forbidden_matches)} matches): {sorted(set(forbidden_matches))}",
                )
            )

        tier2_errors = [i for i in result.issues if i.tier == 2 and i.severity == "ERROR"]
        result.passed_tier2 = len(tier2_errors) == 0

        # --- Tier 3: Structural Lifecycle & Domain Customization ---
        lines = [l.strip() for l in content.splitlines() if l.strip()]

        # 1. Opening role identification
        first_line = lines[0] if lines else ""
        if not first_line.startswith("You are AutoExpert"):
            result.issues.append(
                ValidationIssue(
                    tier=3,
                    rule="AutoExpertOpening",
                    message=f"Opening line must start with 'You are AutoExpert', got: '{first_line[:40]}...'",
                )
            )
        if "skip generic ai behavior" not in first_line.lower():
            result.issues.append(
                ValidationIssue(
                    tier=3,
                    rule="SkipGenericAIBehavior",
                    message="Opening line must mandate skipping generic AI behavior",
                )
            )

        # 2. 5-step lifecycle markers
        # STEP 1
        if not re.search(r"STEP 1\s*[—\-:]\s*PREAMBLE", content, re.IGNORECASE):
            result.issues.append(
                ValidationIssue(tier=3, rule="Step1Preamble", message="Missing STEP 1 — PREAMBLE marker")
            )
        # STEP 2
        if not re.search(r"STEP 2\s*[—\-:]", content, re.IGNORECASE) or "continuing:" not in content.lower():
            result.issues.append(
                ValidationIssue(tier=3, rule="Step2Continuation", message="Missing STEP 2 Continuation marker")
            )
        # STEP 3
        if not re.search(r"STEP 3\s*[—\-:]", content, re.IGNORECASE):
            result.issues.append(
                ValidationIssue(tier=3, rule="Step3Execution", message="Missing STEP 3 Execution marker")
            )
        # STEP 4
        if not re.search(r"STEP 4\s*[—\-:]", content, re.IGNORECASE) or "see also:" not in content.lower():
            result.issues.append(
                ValidationIssue(tier=3, rule="Step4Resources", message="Missing STEP 4 Resource Discovery marker")
            )
        # STEP 5
        if not re.search(r"STEP 5\s*[—\-:]", content, re.IGNORECASE) or "continue?" not in content.lower():
            result.issues.append(
                ValidationIssue(tier=3, rule="Step5Continuation", message="Missing STEP 5 Continuation Prompt marker")
            )

        # 3. Explicit filled-in preamble example
        has_expert = bool(re.search(r"Expert:\s*[^\[\r\n\s][^\[\r\n]*", content))
        has_v = bool(re.search(r"V:\s*[^\[\r\n]*?[0-5]", content))
        has_goal = bool(re.search(r"Goal:\s*[^\[\r\n\s][^\[\r\n]*", content))
        has_plan = bool(re.search(r"Plan:\s*[^\[\r\n]*?(?:1\.|\d\.)", content))
        if not (has_expert and has_v and has_goal and has_plan):
            missing_fields = []
            if not has_expert:
                missing_fields.append("Expert (concrete value)")
            if not has_v:
                missing_fields.append("V (concrete level)")
            if not has_goal:
                missing_fields.append("Goal (concrete statement)")
            if not has_plan:
                missing_fields.append("Plan (numbered steps e.g. 1.)")
            result.issues.append(
                ValidationIssue(
                    tier=3,
                    rule="FilledPreambleExample",
                    message=f"Incomplete filled-in preamble example. Missing fields: {', '.join(missing_fields)}",
                )
            )

        # 4. VERBOSITY dual scale present
        if "VERBOSITY" not in content:
            result.issues.append(
                ValidationIssue(tier=3, rule="VerbositySection", message="Missing VERBOSITY definition section")
            )
        else:
            for level in ["V=1", "V=2", "V=3"]:
                if level not in content:
                    result.issues.append(
                        ValidationIssue(
                            tier=3,
                            rule="VerbosityLevels",
                            message=f"Missing verbosity level definition: {level}",
                        )
                    )

        # 5. Domain rules and epilogue replacing CODING RULES/EPILOGUE for non-technical domains
        is_technical = spec["technical"]
        rules_match = re.search(r"\b[A-Z\s&/\-]+RULES(?:\s*\([^)]*\))?:", content)
        epilogue_match = re.search(r"\b[A-Z\s&/\-]+EPILOGUE(?:\s*\([^)]*\))?:", content)

        if not rules_match:
            result.issues.append(
                ValidationIssue(tier=3, rule="DomainRulesPresent", message="Missing domain operating RULES section")
            )
        if not epilogue_match:
            result.issues.append(
                ValidationIssue(tier=3, rule="DomainEpiloguePresent", message="Missing domain EPILOGUE tracking section")
            )

        if not is_technical:
            if "CODING RULES:" in content:
                result.issues.append(
                    ValidationIssue(
                        tier=3,
                        rule="NonTechnicalRulesAdaptation",
                        message="Non-technical domain must NOT retain generic 'CODING RULES:'; must use domain-specific rules",
                    )
                )
            if "CODING EPILOGUE:" in content:
                result.issues.append(
                    ValidationIssue(
                        tier=3,
                        rule="NonTechnicalEpilogueAdaptation",
                        message="Non-technical domain must NOT retain generic 'CODING EPILOGUE:'; must use domain-specific epilogue",
                    )
                )

        # 6. Universal and domain slash commands
        for cmd in UNIVERSAL_COMMANDS:
            if cmd not in content:
                result.issues.append(
                    ValidationIssue(
                        tier=3,
                        rule="UniversalSlashCommands",
                        message=f"Missing mandatory universal command: {cmd}",
                    )
                )

        # Count total slash commands defined
        found_commands = re.findall(r"(/\b[a-z0-9_]+)\b", content)
        unique_commands = set(found_commands)
        if len(unique_commands) < 8:
            result.issues.append(
                ValidationIssue(
                    tier=3,
                    rule="DomainSlashCommandsCount",
                    message=f"Expected at least 8 slash commands, found only {len(unique_commands)}: {sorted(unique_commands)}",
                )
            )

        # 7. Response footer directive
        if not re.search(r"End every completed response with 2-3 suggested slash commands", content, re.IGNORECASE):
            result.issues.append(
                ValidationIssue(
                    tier=3,
                    rule="SlashCommandsFooterDirective",
                    message="Missing concluding directive to suggest 2-3 slash commands at the end of completed responses",
                )
            )

        tier3_errors = [i for i in result.issues if i.tier == 3 and i.severity == "ERROR"]
        result.passed_tier3 = len(tier3_errors) == 0

        # Mark tier 4 as passed for individual variant if tiers 1-3 passed
        result.passed_tier4 = result.passed_tier1 and result.passed_tier2 and result.passed_tier3

        return result

    def validate_readme(self) -> FileValidationResult:
        result = FileValidationResult(filename=README_FILE)
        filepath = self.target_dir / README_FILE

        # Tier 1
        if not filepath.exists() or not filepath.is_file():
            result.issues.append(
                ValidationIssue(tier=1, rule="ReadmeExistence", message=f"README.txt missing at {filepath}")
            )
            return result

        result.exists = True
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as exc:
            result.issues.append(
                ValidationIssue(tier=1, rule="ReadmeReadability", message=f"Failed to read README.txt: {exc}")
            )
            return result

        if not content.strip():
            result.issues.append(
                ValidationIssue(tier=1, rule="ReadmeNotEmpty", message="README.txt is empty")
            )
            return result

        result.passed_tier1 = True

        # Tier 2
        words = content.split()
        result.word_count = len(words)

        if "#" in content:
            result.issues.append(
                ValidationIssue(
                    tier=2,
                    rule="ZeroMarkdownHashInReadme",
                    message=f"Markdown forbidden character '#' detected in README.txt ({content.count('#')} count)",
                )
            )
        if "**" in content:
            result.issues.append(
                ValidationIssue(
                    tier=2,
                    rule="ZeroMarkdownBoldInReadme",
                    message=f"Markdown forbidden character '**' detected in README.txt ({content.count('**')} count)",
                )
            )

        forbidden_matches = FORBIDDEN_TERMS_PATTERN.findall(content)
        if forbidden_matches:
            result.issues.append(
                ValidationIssue(
                    tier=2,
                    rule="ZeroForbiddenTermsInReadme",
                    message=f"Forbidden vocabulary detected in README.txt: {sorted(set(forbidden_matches))}",
                )
            )

        tier2_errors = [i for i in result.issues if i.tier == 2 and i.severity == "ERROR"]
        result.passed_tier2 = len(tier2_errors) == 0

        # Tier 4: README Master Index requirements
        missing_variants_in_readme = []
        for variant_name in ALL_VARIANT_FILES:
            if variant_name not in content:
                missing_variants_in_readme.append(variant_name)

        if missing_variants_in_readme:
            result.issues.append(
                ValidationIssue(
                    tier=4,
                    rule="ReadmeVariantsInventory",
                    message=f"README.txt missing references to {len(missing_variants_in_readme)} variants: {missing_variants_in_readme}",
                )
            )

        # Check for selection/guidance section
        has_guidance = bool(
            re.search(r"(guidance|when to use|selection guide|choosing a variant|which to use)", content, re.IGNORECASE)
        )
        if not has_guidance:
            result.issues.append(
                ValidationIssue(
                    tier=4,
                    rule="ReadmeSelectionGuidance",
                    message="README.txt missing domain selection guidance / 'when to use' section",
                )
            )

        tier4_errors = [i for i in result.issues if i.tier == 4 and i.severity == "ERROR"]
        result.passed_tier3 = True
        result.passed_tier4 = len(tier4_errors) == 0

        return result

    def validate_pack(
        self,
        batch: Optional[str] = "all",
        tier_filter: Optional[str] = "all",
        variant_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Runs comprehensive validation across the selected scope.
        """
        results: Dict[str, FileValidationResult] = {}

        # Determine which files to validate
        target_files: List[str] = []

        if variant_filter:
            target_files = [variant_filter]
        elif batch == "readme":
            target_files = [README_FILE]
        elif batch in ("1", "2", "3", "4"):
            batch_num = int(batch)
            target_files = [f for f, meta in VARIANT_SPECIFICATIONS.items() if meta["batch"] == batch_num]
        else:  # all
            target_files = list(ALL_PACK_FILES)

        # Run validation
        for fname in target_files:
            if fname == README_FILE:
                results[fname] = self.validate_readme()
            else:
                results[fname] = self.validate_variant_file(fname)

        # Calculate metrics
        total_files = len(target_files)
        passed_files = sum(1 for r in results.values() if r.is_valid)
        failed_files = total_files - passed_files

        tier1_passed = sum(1 for r in results.values() if r.passed_tier1)
        tier2_passed = sum(1 for r in results.values() if r.passed_tier2)
        tier3_passed = sum(1 for r in results.values() if r.passed_tier3)
        tier4_passed = sum(1 for r in results.values() if r.passed_tier4)

        all_issues = [
            {"file": fname, "tier": issue.tier, "rule": issue.rule, "message": issue.message, "severity": issue.severity}
            for fname, r in results.items()
            for issue in r.issues
        ]

        summary = {
            "target_dir": str(self.target_dir),
            "batch": batch,
            "total_files": total_files,
            "passed_files": passed_files,
            "failed_files": failed_files,
            "tier1_pass_count": tier1_passed,
            "tier2_pass_count": tier2_passed,
            "tier3_pass_count": tier3_passed,
            "tier4_pass_count": tier4_passed,
            "status": "PASS" if failed_files == 0 else "FAIL",
            "results": {fname: asdict(r) for fname, r in results.items()},
            "issues": all_issues,
        }
        return summary


# --- Self-Test Fixtures for Harness Self-Verification ---

VALID_SAMPLE_TECHNICAL = """You are AutoExpert, the user's Principal Software Architect & Lead Pair Programmer. Skip generic AI behavior, corporate hedging, and filler.

STEP 1 — PREAMBLE (mandatory on first response to each new query):
Expert: [specific domain authority, not "helpful assistant"]
V: [active verbosity level]
Goal: [refined restatement of what the user actually needs]
Plan: [numbered steps you will follow]

Example:
Expert: Principal Distributed Systems Engineer
V: 3
Goal: Implement a distributed rate limiter using Redis
Plan: 1. Design token bucket algorithm; 2. Write Redis Lua script; 3. Implement middleware

STEP 2 — If continuing from a prior response, open with:
> Continuing: [what this response covers]

STEP 3 — Deliver your answer as the identified expert. Prefix with a relevant emoji. No disclaimers, no apologies. Embed search hyperlinks around key terms where grounding helps. Do not elide code.

STEP 4 — When the answer is complete, append:
See also: 2-3 related topics with links
You may also enjoy: 1-2 tangential or surprising related topics

STEP 5 — If another response is needed:
> Continue? [what comes next]

VERBOSITY (user sets with V=N):
Knowledge: V=1 bullets only, V=2 concise, V=3 balanced (default), V=4 deep dive, V=5 exhaustive academic
Code: V=0 concise, V=1 concise, V=2 standard (default), V=3 verbose DRY with docstrings

CODING RULES:
- Line 1 of every code block: file path comment (e.g. // src/auth.ts or // api/routes.go)
- Never write placeholder comments like "// ... rest unchanged ..." — emit complete runnable files
- Dates: ISO 8601 only (YYYY-MM-DD). Currencies: ISO 4217 (USD, EUR). Units: SI metric.

CODING EPILOGUE (end of substantial coding turns):
Turn: [what was accomplished]
Source Tree: saved file.ext, unsaved file.ext, planned file.ext, tested symbol(), blocked symbol()
Next: [immediate next task]

SLASH COMMANDS (execute immediately when user types one):
/help = show current expert, verbosity, available commands
/v N = change verbosity
/as Role = switch expert persona
/review = critically audit previous response
/plan = phased implementation roadmap
/summary = executive summary, 3 bullets max
/refactor = optimize for performance and DRY
/test = generate unit and integration test fixtures

End every completed response with 2-3 suggested slash commands relevant to the topic.
"""

VALID_SAMPLE_NON_TECHNICAL = """You are AutoExpert, the user's Senior Legal Counsel & Regulatory Compliance Strategist. Skip generic AI behavior, corporate hedging, and filler.

STEP 1 — PREAMBLE (mandatory on first response to each new query):
Expert: [specific domain authority, not "helpful assistant"]
V: [active verbosity level]
Goal: [refined restatement of what the user actually needs]
Plan: [numbered steps you will follow]

Example:
Expert: Senior Commercial Contracts Attorney & Data Privacy Counsel
V: 3
Goal: Review enterprise software agreement for cross-border data transfer compliance
Plan: 1. Analyze data processing addendum; 2. Check Standard Contractual Clauses; 3. Draft liability cap amendment

STEP 2 — If continuing from a prior response, open with:
> Continuing: [what this response covers]

STEP 3 — Deliver your answer as the identified expert. Prefix with a relevant emoji. No disclaimers, no apologies. Embed search hyperlinks around key terms where grounding helps.

STEP 4 — When the answer is complete, append:
See also: 2-3 related topics with links
You may also enjoy: 1-2 tangential or surprising related topics

STEP 5 — If another response is needed:
> Continue? [what comes next]

VERBOSITY (user sets with V=N):
Analysis: V=1 bullets only, V=2 concise, V=3 balanced (default), V=4 deep dive, V=5 exhaustive academic
Drafting: V=1 outline, V=2 summary provisions, V=3 standard commercial clauses, V=4 comprehensive terms

JURISPRUDENTIAL & CONTRACT RULES:
- Cite primary authority: statutes, governing regulations, or binding case precedent.
- Draft unambiguous operative provisions; never emit placeholder clauses like "insert indemnity".
- Differentiate binding jurisdictional authority from persuasive or advisory guidance.
- Dates: ISO 8601 only (YYYY-MM-DD). Currencies: ISO 4217 (USD, EUR). Units: SI metric.

LEGAL EPILOGUE (end of substantial legal turns):
Turn: [what was drafted or reviewed]
Matter Docket: drafted clause.section, reviewed contract.pdf, cited statute(), flagged liability()
Next: [next redline negotiation point or filing milestone]

SLASH COMMANDS (execute immediately when user types one):
/help = show current expert, verbosity, available commands
/v N = change verbosity
/as Role = switch expert persona
/review = critically audit previous response
/summary = executive summary, 3 bullets max
/cite = verify and format primary statutory and case citations
/redline = propose contract language revisions with rationale
/risk = evaluate liability exposure, ambiguity, and dispute probability

End every completed response with 2-3 suggested slash commands relevant to the topic.
"""


def run_self_test() -> bool:
    """
    Executes an internal validation suite against synthetic fixtures to prove
    that every rule and threshold in the test runner functions accurately.
    """
    import tempfile

    print("================================================================================")
    print("RUNNING HARNESS SELF-TEST (VERIFYING VALIDATOR INTEGRITY)")
    print("================================================================================")

    with tempfile.TemporaryDirectory() as tmpdir:
        td = Path(tmpdir)
        validator = VariantPackValidator(td)

        # Test Case 1: Valid technical variant passes
        sw_file = td / "software_engineering.txt"
        sw_file.write_text(VALID_SAMPLE_TECHNICAL, encoding="utf-8")
        res1 = validator.validate_variant_file("software_engineering.txt")
        assert res1.is_valid, f"Expected valid technical file to pass, got issues: {res1.issues}"
        print("  [PASS] Valid technical variant passed all 4 tiers")

        # Test Case 2: Valid non-technical variant passes
        legal_file = td / "legal.txt"
        legal_file.write_text(VALID_SAMPLE_NON_TECHNICAL, encoding="utf-8")
        res2 = validator.validate_variant_file("legal.txt")
        assert res2.is_valid, f"Expected valid non-technical file to pass, got issues: {res2.issues}"
        print("  [PASS] Valid non-technical variant passed all 4 tiers")

        # Test Case 3: Over 500 words fails Tier 2 word count
        long_content = VALID_SAMPLE_TECHNICAL + "\n" + " ".join(["extraWord"] * 250)
        long_file = td / "software_engineering.txt"
        long_file.write_text(long_content, encoding="utf-8")
        res3 = validator.validate_variant_file("software_engineering.txt")
        assert not res3.passed_tier2, "Expected >500 words to fail Tier 2"
        assert any(i.rule == "WordCountBounds" for i in res3.issues), "Missing WordCountBounds issue"
        print(f"  [PASS] Caught word count violation (> 500 words): {res3.word_count} words")

        # Test Case 4: Markdown '#' fails Tier 2
        hash_content = VALID_SAMPLE_TECHNICAL.replace("CODING RULES:", "# CODING RULES:")
        sw_file.write_text(hash_content, encoding="utf-8")
        res4 = validator.validate_variant_file("software_engineering.txt")
        assert any(i.rule == "ZeroMarkdownHash" for i in res4.issues), "Missing ZeroMarkdownHash issue"
        print("  [PASS] Caught forbidden markdown character '#'")

        # Test Case 5: Markdown '**' fails Tier 2
        bold_content = VALID_SAMPLE_TECHNICAL.replace("Expert:", "**Expert:**")
        sw_file.write_text(bold_content, encoding="utf-8")
        res5 = validator.validate_variant_file("software_engineering.txt")
        assert any(i.rule == "ZeroMarkdownBold" for i in res5.issues), "Missing ZeroMarkdownBold issue"
        print("  [PASS] Caught forbidden markdown characters '**'")

        # Test Case 6: Forbidden term 'dossier' fails Tier 2
        forbidden_content = VALID_SAMPLE_NON_TECHNICAL.replace("Matter Docket:", "Matter Dossier:")
        legal_file.write_text(forbidden_content, encoding="utf-8")
        res6 = validator.validate_variant_file("legal.txt")
        assert any(i.rule == "ZeroForbiddenTerms" for i in res6.issues), "Missing ZeroForbiddenTerms issue"
        print("  [PASS] Caught forbidden vocabulary term")

        # Test Case 7: Missing STEP 3 fails Tier 3
        no_step3 = VALID_SAMPLE_TECHNICAL.replace("STEP 3 — Deliver your answer", "DELIVER your answer")
        sw_file.write_text(no_step3, encoding="utf-8")
        res7 = validator.validate_variant_file("software_engineering.txt")
        assert any(i.rule == "Step3Execution" for i in res7.issues), "Missing Step3Execution issue"
        print("  [PASS] Caught missing STEP 3 lifecycle marker")

        # Test Case 8: Non-technical retaining CODING RULES fails Tier 3
        bad_legal = VALID_SAMPLE_NON_TECHNICAL.replace("JURISPRUDENTIAL & CONTRACT RULES:", "CODING RULES:")
        legal_file.write_text(bad_legal, encoding="utf-8")
        res8 = validator.validate_variant_file("legal.txt")
        assert any(i.rule == "NonTechnicalRulesAdaptation" for i in res8.issues), "Missing NonTechnicalRulesAdaptation issue"
        print("  [PASS] Caught unadapted CODING RULES in non-technical domain")

        # Test Case 9: Missing universal slash command fails Tier 3
        no_help = VALID_SAMPLE_TECHNICAL.replace("/help = show current expert", "/info = show current expert")
        sw_file.write_text(no_help, encoding="utf-8")
        res9 = validator.validate_variant_file("software_engineering.txt")
        assert any(i.rule == "UniversalSlashCommands" for i in res9.issues), "Missing UniversalSlashCommands issue"
        print("  [PASS] Caught missing universal slash command (/help)")

        # Test Case 10: Valid README passes Tier 4
        readme_content = "AutoExpert Variants Pack Index\n\nSelection guidance: choose your domain variant.\n\n"
        for vf in ALL_VARIANT_FILES:
            readme_content += f"- {vf}: Domain variant prompt for AutoExpert.\n"
        readme_file = td / README_FILE
        readme_file.write_text(readme_content, encoding="utf-8")
        res10 = validator.validate_readme()
        assert res10.is_valid, f"Expected valid README to pass, got: {res10.issues}"
        print("  [PASS] Valid README passed Tier 4")

        # Test Case 11: Incomplete README fails Tier 4
        truncated_readme = "AutoExpert Variants Pack Index\n- general_qa.txt: General QA.\n"
        readme_file.write_text(truncated_readme, encoding="utf-8")
        res11 = validator.validate_readme()
        assert any(i.rule == "ReadmeVariantsInventory" for i in res11.issues), "Missing ReadmeVariantsInventory issue"
        print("  [PASS] Caught incomplete README inventory")

    print("================================================================================")
    print("ALL HARNESS SELF-TESTS PASSED (11/11 ASSERTIONS CONFIRMED)")
    print("================================================================================")
    return True


# --- Pytest Integration ---

def pytest_generate_tests(metafunc):
    """
    Parametrizes test functions for pytest execution.
    """
    variants_dir = Path(os.environ.get("AUTOEXPERT_VARIANTS_DIR", DEFAULT_VARIANTS_DIR))
    if "variant_filename" in metafunc.fixturenames:
        metafunc.parametrize("variant_filename", ALL_VARIANT_FILES)


def test_tier1_existence_and_readability(variant_filename):
    """
    Tier 1: Verify file existence and UTF-8 readability.
    """
    variants_dir = Path(os.environ.get("AUTOEXPERT_VARIANTS_DIR", DEFAULT_VARIANTS_DIR))
    validator = VariantPackValidator(variants_dir)
    result = validator.validate_variant_file(variant_filename)
    assert result.exists, f"{variant_filename} does not exist at {variants_dir / variant_filename}"
    assert result.passed_tier1, f"{variant_filename} failed Tier 1: {[i.message for i in result.issues if i.tier == 1]}"


def test_tier2_boundary_and_formatting(variant_filename):
    """
    Tier 2: Verify word count < 500, zero '#', zero '**', zero forbidden terms.
    """
    variants_dir = Path(os.environ.get("AUTOEXPERT_VARIANTS_DIR", DEFAULT_VARIANTS_DIR))
    validator = VariantPackValidator(variants_dir)
    result = validator.validate_variant_file(variant_filename)
    if not result.exists:
        import pytest
        pytest.fail(f"Variant file missing: {variant_filename}")
    tier2_issues = [i for i in result.issues if i.tier == 2]
    assert len(tier2_issues) == 0, f"{variant_filename} Tier 2 violations: {[i.message for i in tier2_issues]}"


def test_tier3_lifecycle_and_customization(variant_filename):
    """
    Tier 3: Verify 5-step lifecycle, preamble example, verbosity scale, domain rules/epilogue, slash commands.
    """
    variants_dir = Path(os.environ.get("AUTOEXPERT_VARIANTS_DIR", DEFAULT_VARIANTS_DIR))
    validator = VariantPackValidator(variants_dir)
    result = validator.validate_variant_file(variant_filename)
    if not result.exists:
        import pytest
        pytest.fail(f"Variant file missing: {variant_filename}")
    tier3_issues = [i for i in result.issues if i.tier == 3]
    assert len(tier3_issues) == 0, f"{variant_filename} Tier 3 violations: {[i.message for i in tier3_issues]}"


def test_tier4_readme_integrity():
    """
    Tier 4: Verify README.txt existence, completeness, formatting, and selection guidance.
    """
    variants_dir = Path(os.environ.get("AUTOEXPERT_VARIANTS_DIR", DEFAULT_VARIANTS_DIR))
    validator = VariantPackValidator(variants_dir)
    result = validator.validate_readme()
    assert result.exists, f"README.txt missing at {variants_dir / README_FILE}"
    assert result.is_valid, f"README.txt violations: {[i.message for i in result.issues]}"


# --- CLI Interface & Formatting ---

def print_human_report(summary: Dict[str, Any], verbose: bool = False):
    print("=" * 80)
    print(" AUTOEXPERT VARIANTS PACK — E2E TEST VALIDATION REPORT")
    print("=" * 80)
    print(f" Target Directory: {summary['target_dir']}")
    print(f" Batch Filter:     {summary['batch']}")
    print(f" Overall Status:   {summary['status']}")
    print(f" Files Tested:     {summary['total_files']}")
    print(f" Passed:           {summary['passed_files']} / {summary['total_files']}")
    print(f" Failed:           {summary['failed_files']} / {summary['total_files']}")
    print("-" * 80)
    print(f" Tier 1 (Existence & Basic Content):  {summary['tier1_pass_count']} / {summary['total_files']} passed")
    print(f" Tier 2 (Boundary & Formatting):      {summary['tier2_pass_count']} / {summary['total_files']} passed")
    print(f" Tier 3 (Lifecycle & Customization):  {summary['tier3_pass_count']} / {summary['total_files']} passed")
    print(f" Tier 4 (README & Master Index):      {summary['tier4_pass_count']} / {summary['total_files']} passed")
    print("=" * 80)

    # Per-file breakdown
    print(f"{'Filename':<28} | {'Words':<6} | {'T1':<4} | {'T2':<4} | {'T3':<4} | {'T4':<4} | {'Status':<6}")
    print("-" * 80)
    for fname, r in summary["results"].items():
        t1 = "PASS" if r["passed_tier1"] else "FAIL"
        t2 = "PASS" if r["passed_tier2"] else "FAIL"
        t3 = "PASS" if r["passed_tier3"] else "FAIL"
        t4 = "PASS" if r["passed_tier4"] else "FAIL"
        status = "PASS" if (r["passed_tier1"] and r["passed_tier2"] and r["passed_tier3"] and r["passed_tier4"]) else "FAIL"
        words_str = str(r["word_count"]) if r["exists"] else "-"
        print(f"{fname:<28} | {words_str:<6} | {t1:<4} | {t2:<4} | {t3:<4} | {t4:<4} | {status:<6}")

    # Detailed issues
    if summary["issues"]:
        print("=" * 80)
        print(f" DIAGNOSTIC ISSUES FOUND ({len(summary['issues'])} issue(s)):")
        print("=" * 80)
        for idx, issue in enumerate(summary["issues"], start=1):
            print(f"[{idx}] {issue['file']} (Tier {issue['tier']} - {issue['rule']}):")
            print(f"    {issue['message']}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="AutoExpert Variants Pack Automated E2E Test Suite and Validator"
    )
    parser.add_argument(
        "--target-dir",
        type=str,
        default=str(DEFAULT_VARIANTS_DIR),
        help=f"Path to variants directory (default: {DEFAULT_VARIANTS_DIR})",
    )
    parser.add_argument(
        "--batch",
        type=str,
        default="all",
        choices=["all", "1", "2", "3", "4", "readme"],
        help="Validate a specific milestone batch (default: all)",
    )
    parser.add_argument(
        "--variant",
        type=str,
        default=None,
        help="Validate a specific variant filename (e.g. software_engineering.txt)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit output as structured JSON",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run harness internal self-test against synthetic fixtures",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display verbose diagnostic outputs",
    )

    args = parser.parse_args()

    if args.self_test:
        success = run_self_test()
        sys.exit(0 if success else 1)

    target_dir = Path(args.target_dir).expanduser().resolve()
    validator = VariantPackValidator(target_dir)

    summary = validator.validate_pack(
        batch=args.batch,
        variant_filter=args.variant,
    )

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_human_report(summary, verbose=args.verbose)

    sys.exit(0 if summary["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
