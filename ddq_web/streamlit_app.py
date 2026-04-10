"""
BTSF DDQ Automation — Interface Streamlit
Lance avec : streamlit run streamlit_app.py
Accès : http://localhost:8501
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path
from collections import Counter

import streamlit as st

# ── Config page ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BTSF DDQ Automation",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .header-box {
    background: #0D1F3C; color: white; padding: 20px 28px;
    border-radius: 10px; margin-bottom: 24px;
  }
  .header-box h1 { font-size: 22px; font-weight: 700; margin: 0; }
  .header-box p  { font-size: 13px; color: #9DB4CC; margin: 4px 0 0; }

  .section-title {
    font-size: 11px; font-weight: 700; color: #2E5FA3;
    text-transform: uppercase; letter-spacing: 0.8px;
    border-bottom: 2px solid #B8942A; padding-bottom: 6px;
    margin-bottom: 14px;
  }

  .stat-row { display: flex; gap: 12px; margin: 12px 0; }
  .stat-box { flex:1; padding:12px; border-radius:8px; text-align:center; }
  .stat-box .num { font-size:24px; font-weight:700; }
  .stat-box .lbl { font-size:11px; margin-top:3px; }
  .stat-total   { background:#EEF2F8; color:#0D1F3C; }
  .stat-ok      { background:#EAF5EE; color:#1D6A3A; }
  .stat-partial { background:#FEF9E7; color:#B7770D; }
  .stat-gap     { background:#FDEDEC; color:#C0392B; }

  .sig-active   { display:inline-block; background:#0D1F3C; color:white;
                  padding:3px 10px; border-radius:12px; font-size:11px;
                  font-weight:700; margin:3px; }
  .sig-inactive { display:inline-block; background:#F4F5F7; color:#5A6472;
                  padding:3px 10px; border-radius:12px; font-size:11px; margin:3px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
  <h1>⚡ BTSF — DDQ Automation Tool</h1>
  <p>Bitcoin Mining Credit Due Diligence · v1.1</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar — Clé API ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 Configuration")
    api_key = st.text_input(
        "Clé API Anthropic",
        type="password",
        placeholder="sk-ant-...",
        help="Obtenir sur console.anthropic.com"
    )
    if api_key:
        st.success("Clé configurée ✓")
    else:
        st.warning("Clé API requise")

    st.markdown("---")
    st.markdown("### 📖 Guide rapide")
    st.markdown("""
1. Saisir la clé API
2. Remplir les infos du deal
3. Uploader les documents
4. Ajuster les signaux si besoin
5. Cliquer sur **Générer**
6. Télécharger le Word
    """)


# ── Formulaire ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Informations du deal</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    deal_name = st.text_input("Nom du deal *", value="Project Broadstone",
                               placeholder="Project Broadstone")
with col2:
    mw = st.text_input("Capacité (MW)", placeholder="65 MW")

site = st.text_input("Adresse du site", placeholder="2501 S. Grandview Ave, Odessa TX")

# ── Upload documents ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title" style="margin-top:20px">Documents de la data room</div>',
            unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Glisser-déposer ou sélectionner les fichiers",
    accept_multiple_files=True,
    type=["pdf", "docx", "doc", "xlsx", "xls", "txt", "csv", "md"],
    help="PDF, DOCX, XLSX, TXT acceptés"
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} fichier(s) chargé(s) ✓")
    for f in uploaded_files:
        st.caption(f"📄 {f.name}  —  {f.size // 1024} KB")

# ── Signaux override ──────────────────────────────────────────────────────────
with st.expander("⚙️ Forcer des signaux (optionnel)", expanded=False):
    st.caption("Coché = forcé ON · Décoché et grisé = auto-détecté")

    SIGNAL_LABELS = {
        "greenfield":              "Greenfield (pas d'infra existante)",
        "brownfield":              "Brownfield (site industriel ancien)",
        "existing_infrastructure": "Infrastructure électrique existante",
        "btm_gas":                 "Génération BTM gaz",
        "btm_renewable":           "Génération BTM solaire/éolien",
        "hosting":                 "Opérations d'hébergement (hosting)",
        "existing_debt":           "Dette existante / covenants",
        "permits_in_place":        "Permis déjà obtenus",
        "equipment_purchased":     "Équipement déjà acheté",
        "prior_operations":        "Opérations antérieures sur le site",
        "ppa_present":             "PPA ou contrat énergie fixe",
    }

    forced_on  = []
    forced_off = []
    cols = st.columns(2)
    for i, (key, label) in enumerate(SIGNAL_LABELS.items()):
        col = cols[i % 2]
        val = col.selectbox(
            label,
            options=["Auto-détecté", "Forcer ON ✓", "Forcer OFF ✗"],
            key=f"sig_{key}",
        )
        if val == "Forcer ON ✓":  forced_on.append(key)
        if val == "Forcer OFF ✗": forced_off.append(key)

    signals_override = ",".join(
        [f"{k}=true" for k in forced_on] + [f"{k}=false" for k in forced_off]
    )


# ── Bouton de lancement ───────────────────────────────────────────────────────
st.markdown("")
can_run = bool(api_key and deal_name and uploaded_files)
run_btn = st.button(
    "⚡ Générer la DDQ",
    disabled=not can_run,
    use_container_width=True,
    type="primary",
)

if not can_run and not run_btn:
    if not api_key:        st.info("💡 Renseigne ta clé API dans le panneau de gauche.")
    elif not uploaded_files: st.info("💡 Uploade les documents de la data room.")


# ── Pipeline ──────────────────────────────────────────────────────────────────
if run_btn and can_run:

    # Chercher ddq_app dans les dossiers parents
    ddq_app_dir = None
    for parent in [Path(__file__).parent, Path(__file__).parent.parent]:
        candidate = parent / "ddq_app"
        if (candidate / "main.py").exists():
            ddq_app_dir = candidate
            break

    if not ddq_app_dir:
        st.error("Dossier ddq_app introuvable. Vérifier la structure des fichiers.")
        st.stop()

    sys.path.insert(0, str(ddq_app_dir))
    os.environ["ANTHROPIC_API_KEY"] = api_key

    # Dossier temporaire pour les fichiers uploadés
    with tempfile.TemporaryDirectory() as tmpdir:

        # Sauvegarder les fichiers
        for uf in uploaded_files:
            dest = Path(tmpdir) / uf.name
            dest.write_bytes(uf.read())

        # Barres de progression
        progress = st.progress(0)
        status   = st.status("Démarrage du pipeline...", expanded=True)

        try:
            from core.ingestion import ingest_folder
            from core.signals   import detect_signals
            from core.questions import assemble_questions
            from core.generator import generate_answers
            from core.writer    import export_docx
            from main           import parse_signals_override

            # Step 1
            status.write("📂 Extraction des documents...")
            progress.progress(10)
            chunks = ingest_folder(tmpdir)
            status.write(f"✓ {len(chunks)} chunks extraits depuis {len(uploaded_files)} fichier(s)")

            # Step 2
            status.write("🔍 Détection des signaux...")
            progress.progress(25)
            signals = detect_signals(chunks)
            if signals_override:
                overrides = parse_signals_override(signals_override)
                signals.update(overrides)
            active_sigs = [k for k, v in signals.items() if v]
            status.write(f"✓ Signaux détectés : {', '.join(active_sigs) or 'aucun'}")

            # Step 3
            status.write("📋 Assemblage des questions...")
            progress.progress(40)
            questions = assemble_questions(signals)
            status.write(f"✓ {len(questions)} questions assemblées")

            # Step 4
            status.write(f"🤖 Génération des réponses ({len(questions)} questions)...")
            answers = []
            total   = len(questions)
            q_progress = st.progress(0)
            q_status   = st.empty()

            for i, q in enumerate(questions, 1):
                ans = generate_answers([q], chunks, verbose=False)
                answers.extend(ans)
                pct = int(i / total * 100)
                q_progress.progress(pct)
                q_status.caption(f"Question {i}/{total} — {q.qid}: {q.text[:55]}...")
                progress.progress(40 + int((i / total) * 45))

            q_progress.empty()
            q_status.empty()

            counts = Counter(a.confidence for a in answers)
            status.write(f"✓ {counts.get('answered',0)} répondues · "
                         f"{counts.get('partial',0)} partielles · "
                         f"{counts.get('gap',0)} gaps")

            # Step 5
            status.write("📝 Génération du document Word...")
            progress.progress(95)

            site_info = {}
            if site: site_info["Site address"]  = site
            if mw:   site_info["Grid capacity"] = mw

            import config as cfg
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            cfg.OUTPUT_DIR = str(output_dir)

            output_path = export_docx(answers, signals, deal_name, site_info or None)
            progress.progress(100)
            status.update(label="✅ DDQ générée avec succès !", state="complete")

            # ── Résultats ─────────────────────────────────────────────────────
            st.markdown("---")
            st.markdown('<div class="section-title">Résultats</div>', unsafe_allow_html=True)

            # Stats
            st.markdown(f"""
            <div class="stat-row">
              <div class="stat-box stat-total">
                <div class="num">{len(answers)}</div><div class="lbl">Questions</div>
              </div>
              <div class="stat-box stat-ok">
                <div class="num">{counts.get('answered',0)}</div><div class="lbl">Répondues</div>
              </div>
              <div class="stat-box stat-partial">
                <div class="num">{counts.get('partial',0)}</div><div class="lbl">Partielles</div>
              </div>
              <div class="stat-box stat-gap">
                <div class="num">{counts.get('gap',0)}</div><div class="lbl">Gaps</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Signaux détectés
            st.markdown("**Signaux détectés :**")
            sig_html = "".join(
                f'<span class="sig-{"active" if v else "inactive"}">'
                f'{k.replace("_"," ")}</span>'
                for k, v in signals.items()
            )
            st.markdown(sig_html, unsafe_allow_html=True)

            # Bouton téléchargement
            st.markdown("")
            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇️ Télécharger la DDQ (Word)",
                    data=f.read(),
                    file_name=Path(output_path).name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    type="primary",
                )

        except Exception as e:
            progress.empty()
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur : {e}")
            st.exception(e)
