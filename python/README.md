SCORM Security – Gerador de Conteúdo SCORM (Python + Streamlit)

Descrição
- Gerador que transforma uma sequência de imagens de slides em um pacote SCORM 1.2 pronto para upload no seu LMS.
- Player HTML com navegação “Voltar/Próximo” abaixo do slide, visual clean e cor padrão dos botões em `#0022cb`.
- Mensagem final dinâmica (texto em Markdown → HTML). Ao finalizar, o pacote marca o curso como “completed” no LMS e oferece o botão “Sair da Apresentação”.

Principais Recursos
- Entrada por imagens `.png` e `.jpeg/.jpg` nomeadas sequencialmente: `slide-01.png`, `slide-02.jpeg`, `slide-03.png`...
- Pré-visualização do player dentro do app (modal visual), idêntica ao pacote final.
- Geração do pacote `.zip` contendo `index.html`, `imsmanifest.xml`, `static/` (CSS/JS) e a pasta `slides/` com as imagens.
- SCORM 1.2: inicializa o SCO, seta `cmi.core.lesson_status = completed` ao chegar na tela final, faz `LMSCommit` e fecha com `LMSFinish` no botão de saída.

Requisitos
- Python 3.9+
- Dependências: ver `requirements.txt`

Instalação
- Crie e ative um virtualenv (opcional):
  - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
  - Windows (PowerShell): `py -m venv .venv; .\\.venv\\Scripts\\Activate.ps1`
- Instale as dependências:
  - `pip install -r requirements.txt`

Uso
1) Inicie o app Streamlit:
- `streamlit run app.py`

2) Envie os slides
- Use o uploader para selecionar múltiplas imagens com os nomes no padrão `slide-NN.ext` (ex.: `slide-01.png`, `slide-02.jpeg`).

3) Mensagem final
- Escreva a mensagem de conclusão em Markdown (ex.: “Parabéns! Você finalizou este curso com sucesso.”). O app converte para HTML.

4) Pré-visualize
- Clique em “Abrir pré-visualização”. O player abre em modal visual com o mesmo comportamento do pacote final.

5) Gere o pacote SCORM
- Clique em “Gerar e baixar .zip” para baixar o pacote e subir no seu LMS.

Nomeação de Arquivos (Obrigatória)
- Padrão aceito: `^slide-(\d+)\.(png|jpe?g)$` (case-insensitive).
- Exemplos válidos: `slide-01.png`, `slide-2.jpg`, `slide-10.jpeg`.
- Qualquer arquivo fora do padrão é ignorado.

Personalização Rápida
- Cor do botão: por padrão `#0022cb`. No player, a variável CSS é `--btn-color` em `static/styles.css` e no template inline do preview.
- Texto do botão final: “Sair da Apresentação” no estado final do curso.

Estrutura do Projeto
- `app.py`: app Streamlit.
- `scorm/images.py`: leitura/validação/ordenação dos slides enviados.
- `scorm/generator.py`: renderização de `index.html` (Jinja2) e HTML inline do preview.
- `scorm/packaging.py`: `imsmanifest.xml` (inline), CSS/JS padrão e empacotamento no `.zip`.
- `scorm/templates/index.html.j2`: template do player para o pacote.
- `scorm/templates/index_inline.html.j2`: template inline do player para a pré-visualização.
- `scorm/templates/imsmanifest.xml.j2`: manifesto SCORM 1.2 (base para migração futura do inline).
- `scorm/static/styles.css` e `scorm/static/scorm12.js`: estilos e integração SCORM.
- `examples/slides/`: pasta para exemplos locais.

Como Funciona (Player)
- Navegação abaixo do slide com botões “Voltar” (secundário) e “Próximo” (primário azul), e indicador “N de Total”.
- Ao atingir o fim:
  - Esconde “Próximo” e o indicador; mostra a mensagem final e o botão “Sair da Apresentação”.
  - Marca `cmi.core.lesson_status = completed` e faz `LMSCommit`.
  - O botão “Sair da Apresentação” chama `LMSFinish` e tenta fechar a janela.

Compatibilidade e Testes
- Padrão: SCORM 1.2 (testar no seu LMS). Para validação externa, use ferramentas como SCORM Cloud (upload manual do `.zip`).
- Fora de um LMS, o player funciona e as chamadas SCORM falham silenciosamente (sem quebrar a navegação).

Solução de Problemas
- Slides não aparecem: verifique se os nomes seguem o padrão `slide-NN.ext`.
- Preview não abre como modal nativo: o app usa um modal visual compatível com qualquer versão do Streamlit; atualizar o Streamlit não é obrigatório.
- Status não fecha no LMS: alguns navegadores bloqueiam `window.close()` quando o SCO não foi aberto por script; o curso ainda é marcado como concluído.

Roadmap (curto prazo)
- Migrar `render_manifest_12` para uso do template `scorm/templates/imsmanifest.xml.j2`.
- Sanitização leve do HTML gerado a partir do Markdown.
- Opção de alterar a cor dos botões pela interface.

Licença
- MITM
