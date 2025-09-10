    # Observação: mantém recursos básicos com index.html como SCO principal.
from typing import List, Dict


def render_manifest_12(identifier: str, title: str, slides: List[Dict]) -> str:
    """Gera um imsmanifest.xml mínimo para SCORM 1.2."""
    # Template simples inline (será substituído por Jinja2 se necessário)
    # Observação: mantém recursos básicos com index.html como SCO principal.
    return f"""
<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{identifier}" version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="
            http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
            http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <organizations default="ORG1">
    <organization identifier="ORG1">
      <title>{title}</title>
      <item identifier="ITEM1" identifierref="RES1">
        <title>{title}</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES1" type="webcontent" adlcp:scormtype="sco" href="index.html">
      <file href="index.html"/>
      <file href="static/styles.css"/>
      <file href="static/scorm12.js"/>
""" + "\n".join([f"      <file href=\"slides/{s['name']}\"/>" for s in slides]) + "\n" + """
    </resource>
  </resources>
</manifest>
""".strip()


def make_scorm_zip(zf, index_html: str, manifest_xml: str, slides: List[Dict]):
    """Escreve no ZipFile os artefatos mínimos do pacote SCORM."""
    # index.html
    zf.writestr("index.html", index_html)
    # manifest
    zf.writestr("imsmanifest.xml", manifest_xml)
    # estáticos
    zf.writestr("static/styles.css", _DEFAULT_CSS)
    zf.writestr("static/scorm12.js", _DEFAULT_SCORM12_JS)
    # slides
    for s in slides:
        zf.writestr(f"slides/{s['name']}", s["data"]) 


_DEFAULT_CSS = """
:root { --btn-color: #0022cb; --gray-100: #F3F4F6; --gray-300: #E5E7EB; --gray-500: #6B7280; }
html, body { margin: 0; padding: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; background: #fff; color: #111827; }
.wrap { max-width: 960px; margin: 0 auto; padding: 16px; }
.toolbar { display: flex; gap: 12px; align-items: center; justify-content: space-between; margin: 16px 0; padding: 14px; border: 1px solid var(--gray-300); border-radius: 12px; background: #fff; }
.btn { border: 0; border-radius: 12px; padding: 12px 20px; min-height: 44px; font-size: 16px; font-weight: 600; cursor: pointer; line-height: 1; display: inline-flex; align-items: center; }
.btn .chev { font-weight: 700; }
.btn-primary { background: var(--btn-color); color: #fff; min-width: 160px; box-shadow: 0 1px 0 rgba(0,0,0,0.05); }
.btn-primary:hover { filter: brightness(0.95); }
.btn-secondary { background: var(--gray-100); color: var(--gray-500); border: 1px solid var(--gray-300); }
.btn-secondary:hover { background: #E8EAED; }
.btn:disabled { opacity: .6; cursor: not-allowed; }
.btn-primary .chev { margin-left: 8px; }
.btn-secondary .chev { margin-right: 8px; }
.slide { display: flex; align-items: center; justify-content: center; }
.slide img { max-width: 100%; height: auto; }
.progress { font-size: 14px; color: var(--gray-500); flex: 1; text-align: center; }
.final { display: none; }
.final { text-align: center; padding: 24px 0; }
.final-content { margin-bottom: 8px; }
""".strip()


_DEFAULT_SCORM12_JS = """
(function() {
  // Descoberta simples da API SCORM 1.2
  function findAPI(win) {
    var findTries = 0;
    while ((win.API == null) && (win.parent != null) && (win.parent != win) && (findTries < 500)) {
      findTries++;
      win = win.parent;
    }
    return win.API || null;
  }

  window.SCORM = {
    api: null,
    init: function() {
      try {
        this.api = findAPI(window);
        if (this.api && this.api.LMSInitialize) {
          this.api.LMSInitialize("");
        }
      } catch(e) {}
    },
    complete: function() {
      try {
        if (this.api && this.api.LMSSetValue) {
          this.api.LMSSetValue('cmi.core.lesson_status', 'completed');
          this.api.LMSCommit("");
        }
      } catch(e) {}
    },
    finish: function() {
      try {
        if (this.api && this.api.LMSFinish) {
          this.api.LMSFinish("");
        }
      } catch(e) {}
    }
  };
})();
""".strip()
