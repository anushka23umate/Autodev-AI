import json
from typing import Any, Dict


def parse_llm_json(text: str) -> Dict[str, Any]:
    """Parse JSON from LLM response"""
    try:
        # Try to find JSON block in markdown code fence
        if "```json" in text:
            json_start = text.find("```json") + 7
            json_end = text.find("```", json_start)
            json_text = text[json_start:json_end].strip()
        elif "```" in text:
            json_start = text.find("```") + 3
            json_end = text.find("```", json_start)
            json_text = text[json_start:json_end].strip()
        else:
            json_text = text
        
        return json.loads(json_text)
    except json.JSONDecodeError:
        return {}


def format_requirements_dict(reqs: Dict[str, list]) -> str:
    """Format requirements dict to requirements.txt"""
    lines = []
    for package, versions in reqs.items():
        if isinstance(versions, list) and versions:
            lines.append(f"{package}=={versions[0]}")
        elif isinstance(versions, str):
            lines.append(f"{package}=={versions}")
        else:
            lines.append(package)
    return "\n".join(lines)


def format_dependencies_dict(deps: Dict[str, str]) -> str:
    """Format dependencies for package.json"""
    result = {}
    for pkg, version in deps.items():
        if version.startswith("^") or version.startswith("~"):
            result[pkg] = version
        else:
            result[pkg] = f"^{version}"
    return json.dumps(result, indent=2)
