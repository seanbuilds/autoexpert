import re
from pathlib import Path
import os
import subprocess

root = Path('/Volumes/BLK4TB/autoexpert')

# Issue 4: URLs
md_files = [
    root / 'docs/AUTOEXPERT_MASTER_ALL.md',
    root / 'editions/v1-classic/developer/README.md',
    root / 'editions/v1-classic/standard/README.md',
    root / 'editions/v1-classic/system-prompts/gpts/README.md'
]
for p in md_files:
    if p.exists():
        content = p.read_text()
        content = re.sub(
            r'(\(https://chat\.openai\.com/share/[^\)]+\))',
            r'\1 (Original demo links, may no longer be active)',
            content
        )
        p.write_text(content)

# Issue 5: Duplicate Files
skills = [
    ('claude_code', '# AutoExpert Skill: Claude Code Edition\n\nOptimized for Claude Code CLI agent workflows.\n\n'),
    ('open_interpreter', '# AutoExpert Skill: Open Interpreter Edition\n\nOptimized for Open Interpreter local agent workflows.\n\n'),
    ('antigravity', '# AutoExpert Skill: Google Antigravity Edition\n\nCanonical Antigravity agent skill.\n\n')
]

for skill_dir, header in skills:
    skill_file = root / f'formats/agent_skills/{skill_dir}/SKILL.md'
    if skill_file.exists():
        content = skill_file.read_text()
        if not content.startswith('# AutoExpert Skill'):
            skill_file.write_text(header + content)

# Issue 6: Empty Directories
v4_readme = root / 'editions/v4-enterprise-hybrid/README.md'
v4_readme.parent.mkdir(parents=True, exist_ok=True)
v4_readme.write_text("# Enterprise Hybrid Edition\n\nSee `specialized/enterprise/SYSTEM_PROMPT.md` for the enterprise dual-role system prompt.\n\nHistorical compendium documentation is available in `docs/AUTOEXPERT_MASTER_ALL.md` Part V.\n")

claude_dir = root / 'formats/custom_instructions/claude'
claude_dir.mkdir(parents=True, exist_ok=True)
sys_prompt = root / 'core/standard/SYSTEM_PROMPT.md'
if sys_prompt.exists():
    sp_content = sys_prompt.read_text()
    # Extract markdown content from inside the code block
    match = re.search(r'```(?:markdown)?\n(.*?)\n```', sp_content, re.DOTALL)
    if match:
        sp_content = match.group(1)
    
    claude_inst = claude_dir / 'claude_project_instructions.md'
    claude_inst.write_text(f"<autoexpert_instructions>\n{sp_content}\n</autoexpert_instructions>\n")

def get_tree(dir_path, level=2, prefix=''):
    if level == 0:
        return []
    items = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d)) and d not in ['.git', '.pytest_cache', '__pycache__']]
    items.sort()
    lines = []
    for i, item in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = '`-- ' if is_last else '|-- '
        lines.append(prefix + connector + item)
        new_prefix = prefix + ('    ' if is_last else '|   ')
        lines.extend(get_tree(os.path.join(dir_path, item), level - 1, new_prefix))
    return lines

readme = root / 'README.md'
if readme.exists():
    tree_text = '.' + '\n' + '\n'.join(get_tree(str(root)))
    
    content = readme.read_text()
    if '## 📁 Repository Structure' not in content:
        match = re.search(r'(\n\|.*\|\n\|.*\|\n(?:\|.*\|\n)*\n)', content)
        if match:
            insert_pos = match.end()
            new_content = content[:insert_pos] + "## 📁 Repository Structure\n```text\n" + tree_text + "\n```\n\n" + content[insert_pos:]
            readme.write_text(new_content)
        else:
            readme.write_text(content + "\n## 📁 Repository Structure\n```text\n" + tree_text + "\n```\n")
