import os
import re
import glob

import yaml
from openai import OpenAI


_SKILLS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "config", "skills")
)

_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)

_LANG_OPTIONS = ["自动(中文优先)", "中文", "英文"]


def _strip_frontmatter(text: str) -> str:
    return _FRONTMATTER_RE.sub("", text, count=1).strip()


def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _load_meta(skill_dir: str):
    path = os.path.join(skill_dir, "meta.yaml")
    raw = _read_text(path)
    if not raw:
        return {}
    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _list_skills(skills_dir: str = _SKILLS_DIR):
    """Return a list of (folder_name, display_label) sorted by label."""
    if not os.path.isdir(skills_dir):
        return []
    items = []
    for entry in sorted(os.listdir(skills_dir)):
        skill_dir = os.path.join(skills_dir, entry)
        if not os.path.isdir(skill_dir):
            continue
        meta = _load_meta(skill_dir)
        label = meta.get("display-name-zh") or meta.get("display-name") or entry
        items.append((entry, str(label)))
    items.sort(key=lambda x: x[1])
    return items


def _resolve_skill_md(skill_dir: str, lang: str):
    """Return absolute path of the SKILL doc matching the language preference, or None."""
    candidates = []
    if lang == "中文":
        candidates = ["SKILL.cn.md", "SKILL.md"]
    elif lang == "英文":
        candidates = ["SKILL.md", "SKILL.cn.md"]
    else:  # auto: prefer Chinese
        candidates = ["SKILL.cn.md", "SKILL.md"]
    for name in candidates:
        path = os.path.join(skill_dir, name)
        if os.path.isfile(path):
            return path
    return None


def _list_reference_files(skill_dir: str):
    refs_dir = os.path.join(skill_dir, "references")
    if not os.path.isdir(refs_dir):
        return []
    files = []
    for root, _, names in os.walk(refs_dir):
        for name in names:
            if name.startswith("."):
                continue
            files.append(os.path.join(root, name))
    files.sort()
    return files


def _build_skill_prompt(skill_name: str, lang: str, skills_dir: str = _SKILLS_DIR):
    """Compose the system prompt body for the chosen skill.

    Returns (prompt_text, used_label) where used_label describes which file
    was loaded so the caller can surface it.
    """
    if not skill_name:
        return "", ""
    safe_name = os.path.basename(skill_name)
    skill_dir = os.path.join(skills_dir, safe_name)
    if not os.path.isdir(skill_dir):
        return "", ""

    skill_md_path = _resolve_skill_md(skill_dir, lang)
    if skill_md_path is None:
        return "", ""

    skill_body = _strip_frontmatter(_read_text(skill_md_path))
    if not skill_body:
        return "", ""

    parts = [f"## Skill: {safe_name}", skill_body]

    used_label = os.path.basename(skill_md_path)

    ref_files = _list_reference_files(skill_dir)
    if ref_files:
        ref_blocks = []
        for path in ref_files:
            content = _read_text(path)
            if not content:
                continue
            rel = os.path.relpath(path, skill_dir).replace("\\", "/")
            ref_blocks.append(f"### references/{rel}\n\n{content.strip()}")
        if ref_blocks:
            parts.append("## Reference Material\n\n" + "\n\n".join(ref_blocks))

    return "\n\n".join(parts), used_label


class LamAgent:
    """
    通过 OpenAI 兼容接口调用大模型。
    从 config/skills 下选择一个 skill 子目录，
    SKILL.md (含 references/) 内容会作为 system prompt 注入。
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        skills = _list_skills()
        labels = [label for _, label in skills] if skills else ["(no skills found)"]
        return {
            "required": {
                "server_url": ("STRING", {"default": "https://ark.cn-beijing.volces.com/api/coding/v3"}),
                "api_key": ("STRING", {"default": ""}),
                "model_name": ("STRING", {"default": "deepseek-v4-pro"}),
                "skill": (labels,),
                "language": (_LANG_OPTIONS, {"default": "自动(中文优先)"}),
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("结果",)

    FUNCTION = "chat"

    CATEGORY = "lam"

    def chat(self, server_url, api_key, model_name, skill, language, text):
        # Resolve display label back to the folder name.
        folder_name = skill
        for name, label in _list_skills():
            if label == skill:
                folder_name = name
                break

        skill_prompt, _used = _build_skill_prompt(folder_name, language)
        client = OpenAI(api_key=api_key, base_url=server_url)

        messages = []
        if skill_prompt:
            messages.append({"role": "system", "content": skill_prompt})
        messages.append({"role": "user", "content": text})

        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            top_p=0.8,
            temperature=0.7,
        )
        return (completion.choices[0].message.content,)


NODE_CLASS_MAPPINGS = {
    "LamAgent": LamAgent,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LamAgent": "Lam 智能体",
}
