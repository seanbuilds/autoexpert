import pytest
import os
import json
from tools.autodev.cli import load_stash, save_stash, STASH_FILE

def test_stash_and_recall(tmp_path, monkeypatch):
    test_stash = tmp_path / "test_stash.json"
    monkeypatch.setattr("tools.autodev.cli.STASH_FILE", str(test_stash))
    
    save_stash({"framework": "AutoExpert"})
    data = load_stash()
    assert data.get("framework") == "AutoExpert"

def test_prompt_compiler():
    from tools.prompt_compiler.compiler import generate_system_instruction
    prompt = generate_system_instruction("claude", 4, "Systems Architect")
    assert "Systems Architect" in prompt
    assert "V=4" in prompt
    assert "<autoexpert_instructions>" in prompt
