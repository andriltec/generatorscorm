import io
from pathlib import Path
import zipfile

import streamlit as st
import streamlit.components.v1 as components
from markdown import markdown

# Local modules (stubs implemented under scorm/)
from scorm.images import parse_uploaded_slides
from scorm.generator import render_index_html, render_index_html_inline_preview
from scorm.packaging import render_manifest_12, make_scorm_zip


st.set_page_config(page_title="Gerador SCORM", page_icon="📦", layout="centered")

st.title("Gerador de Conteúdo SCORM (slides → pacote .zip)")
st.caption("Versão inicial – SCORM 1.2")

with st.sidebar:
    st.header("Configurações")
    course_title = st.text_input("Título do curso", value="Meu Curso SCORM")
    course_identifier = st.text_input("Identificador (opcional)", value="")
    button_color = "#0022cb"  # fixo nesta fase

st.subheader("1) Envie as imagens dos slides")
uploaded = st.file_uploader(
    "Imagens (slide-01.png, slide-02.jpeg, …)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
    help="Nomeie os arquivos como slide-01.png, slide-02.jpeg, etc.",
)

st.subheader("2) Mensagem final (Markdown)")
default_md = "Parabéns, você finalizou este curso!"
final_md = st.text_area("Conteúdo final", value=default_md, height=140)

slides = parse_uploaded_slides(uploaded)
if slides and len(slides) > 0:
    st.success(f"{len(slides)} slide(s) reconhecido(s). Ex: {slides[0]['name']}")
    # preview simples
    st.image(slides[0]["data"], caption=slides[0]["name"], use_column_width=True)
else:
    if uploaded:
        st.error("Nenhum arquivo válido encontrado. Verifique a nomeação: slide-NN.png/jpeg.")

st.subheader("3) Pré-visualização do player")
if slides:
    if st.button("Abrir pré-visualização", key="open_preview", type="secondary"):
        st.session_state["preview_open"] = True

    if st.session_state.get("preview_open"):
        preview_html = render_index_html_inline_preview(
            slides=slides,
            course_title=course_title.strip() or "Curso",
            final_message_html=markdown(final_md or default_md),
            button_color=button_color,
        )
        # Modal independente de versão: overlay com iframe data: URL
        import base64
        data_url = "data:text/html;base64," + base64.b64encode(preview_html.encode("utf-8")).decode("ascii")
        overlay = f"""
        <style>
          .overlay {{ position: fixed; inset: 0; background: rgba(0,0,0,0.55); display: flex; align-items: center; justify-content: center; }}
          .modal {{ background: #fff; width: min(1100px, 96vw); height: 92vh; border-radius: 10px; box-shadow: 0 20px 50px rgba(0,0,0,.4); overflow: hidden; }}
          .modal > iframe {{ width: 100%; height: 100%; border: 0; }}
        </style>
        <div class="overlay">
          <div class="modal">
            <iframe src="{data_url}" title="Pré-visualização"></iframe>
          </div>
        </div>
        """
        components.html(overlay, height=1000, scrolling=False)
        if st.button("Fechar pré-visualização", key="close_preview_any"):
            st.session_state["preview_open"] = False
            st.rerun()

st.subheader("4) Gerar pacote SCORM 1.2")
generate = st.button("Gerar e baixar .zip", type="primary", disabled=not slides)

if generate and slides:
    # Render HTML do player
    final_html = markdown(final_md or default_md)
    index_html = render_index_html(
        slides=slides,
        course_title=course_title.strip() or "Curso",
        final_message_html=final_html,
        button_color=button_color,
    )

    # Manifest (SCORM 1.2)
    identifier = (course_identifier or course_title or "curso").strip().lower().replace(" ", "-")
    manifest_xml = render_manifest_12(identifier=identifier or "curso", title=course_title or "Curso", slides=slides)

    # Monta o zip em memória
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        make_scorm_zip(zf=zf, index_html=index_html, manifest_xml=manifest_xml, slides=slides)

    st.download_button(
        label="Baixar pacote SCORM (.zip)",
        data=buf.getvalue(),
        file_name=f"{identifier or 'curso'}.zip",
        mime="application/zip",
    )
