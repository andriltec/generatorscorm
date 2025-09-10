import io
import re
from typing import List, Dict, Any


_PATTERN = re.compile(r"^slide-(\d+)\.(png|jpe?g)$", re.IGNORECASE)


def parse_uploaded_slides(files: List[Any]) -> List[Dict[str, Any]]:
    """
    Recebe a lista de arquivos do Streamlit (UploadedFile) e retorna
    uma lista ordenada por número: [{name, number, data(bytes)}].
    Ignora arquivos que não batem o padrão esperado.
    """
    if not files:
        return []

    parsed = []
    for f in files:
        name = getattr(f, "name", "") or ""
        m = _PATTERN.match(name.strip())
        if not m:
            continue
        try:
            num = int(m.group(1))
        except Exception:
            continue
        data = f.read() if hasattr(f, "read") else None
        if hasattr(f, "seek"):
            try:
                f.seek(0)
            except Exception:
                pass
        if not isinstance(data, (bytes, bytearray)):
            # pode ser que o objeto UploadedFile não tenha read; tenta .getvalue
            data = getattr(f, "getvalue", lambda: b"")()
        if not data:
            continue
        parsed.append({"name": name, "number": num, "data": data})

    parsed.sort(key=lambda x: x["number"])  # ordena por número
    return parsed

