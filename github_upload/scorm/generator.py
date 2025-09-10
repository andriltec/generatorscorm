from pathlib import Path
from typing import List, Dict
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
import base64


def _env() -> Environment:
    base = Path(__file__).parent
    tpl_dir = base / "templates"
    env = Environment(
        loader=FileSystemLoader(str(tpl_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        enable_async=False,
    )
    return env


def render_index_html(
    slides: List[Dict],
    course_title: str,
    final_message_html: str,
    button_color: str = "#0022cb",
) -> str:
    env = _env()
    template = env.get_template("index.html.j2")
    slides_spec = [{"src": f"slides/{s['name']}"} for s in slides]
    slides_json = json.dumps(slides_spec)
    return template.render(
        title=course_title,
        slides_json=slides_json,
        first_src=(slides_spec[0]["src"] if slides_spec else ""),
        total=len(slides_spec),
        final_message_html=final_message_html,
        button_color=button_color,
    )


def _data_uri_for(name: str, data: bytes) -> str:
    mime = "image/png"
    lower = name.lower()
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        mime = "image/jpeg"
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def render_index_html_inline_preview(
    slides: List[Dict],
    course_title: str,
    final_message_html: str,
    button_color: str = "#0022cb",
) -> str:
    env = _env()
    # carrega css/js locais para incorporar
    base = Path(__file__).parent
    css = (base / "static" / "styles.css").read_text(encoding="utf-8")
    js = (base / "static" / "scorm12.js").read_text(encoding="utf-8")

    slides_spec = [{"src": _data_uri_for(s["name"], s["data"])} for s in slides]
    slides_json = json.dumps(slides_spec)
    template = env.get_template("index_inline.html.j2")
    return template.render(
        title=course_title,
        slides_json=slides_json,
        first_src=(slides_spec[0]["src"] if slides_spec else ""),
        total=len(slides_spec),
        final_message_html=final_message_html,
        button_color=button_color,
        css=css,
        js=js,
    )
