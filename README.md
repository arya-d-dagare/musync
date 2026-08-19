# MuSync — Upgraded Music Recommendation System (Research Prototype)

A research-prototype AI-assisted music recommendation system that combines
psychological, physiological, and preference inputs with a hybrid
RNN/NCF/RL fusion engine — with graceful fallbacks so it always runs, and
honest labeling everywhere real data or trained models are missing.

**This is not a medical device.** It does not diagnose or treat any
condition. See `modules/safety.py`.

## 1. What was preserved from the original code

- `modules/models.py` — the original `ContextRNN` (LSTM+attention) and
  `ContextNCF` architectures, byte-for-byte identical to the seniors' design.
- `modules/recommender.py` — the original filtering pipeline (mood/HRV/
  stress audio-feature filters), preference bias, psychology bias, and the
  Q-learning RL update, unchanged in logic.
- `modules/psychology.py` — the original TIPI / DASS-21 / WHOQOL-BREF
  scoring formulas, unchanged, now with a documentation layer added.
- The adaptive feedback loop (Ridge-regression re-weighting once ≥20
  feedback rows exist) is unchanged.

## 2. What's new

| Area | File |
|---|---|
| Graceful Mongo-optional persistence | `modules/config.py`, `modules/local_store.py`, `modules/db.py` |
| Professional non-blue theme | `modules/theme.py` |
| Real HRV feature extraction (SDNN/RMSSD/pNN50/mean RR/HR) | `modules/physiological.py` |
| WESAD loader (interface only — you supply the data) | `modules/physiological.py` |
| Safety layer (confidence gating, adverse-response flagging) | `modules/safety.py` |
| Structured Risk-of-Bias checklist | `modules/bias.py` |
| Real validation metrics computed from actual feedback | `modules/validation.py` |
| Verified evidence base + citations | `modules/evidence.py` |
| Content-based fallback when trained models are absent | `modules/models.py`, `modules/recommender.py` |
| Demo dataset fallback (clearly labeled) | `modules/dataset.py` |

## 3. Run instructions

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app runs immediately with **no configuration at all** — it will use:
local file-based storage instead of MongoDB, a simple name-based sign-in
instead of OTP email, a 12-song demo catalog instead of your real dataset,
and content-based-only scoring instead of the trained RNN/NCF models.
Every one of these fallbacks is shown as a badge in the sidebar and on the
**Dataset / Research Mode** page.

## 4. Putting this on GitHub (exact steps)

**What to upload:** everything in this folder **except** what's already
listed in `.gitignore` — that specifically excludes secrets, generated
local data, and (by default) the large dataset/model files, since those
often exceed GitHub's comfortable file-size limits and shouldn't be
committed alongside code.

```bash
cd musync
git init
git add .
git commit -m "Initial commit: MuSync research prototype"
git branch -M main
git remote add origin https://github.com/<your-username>/musync.git
git push -u origin main
```

That's it — the repo now has all 19 files below, and anyone who clones it
and runs `pip install -r requirements.txt && streamlit run app.py` gets a
fully working app in fallback mode immediately.

**About the large files** (`Music_dataset2.csv`, `metadata2.pth`,
`rnn_model_trained2.pth`, `ncf_model_trained2.pth`) — they're gitignored
on purpose. You have two options:

- **Option A (simplest):** don't commit them. After each teammate clones
  the repo, they drop their own copies of these 4 files into the project
  root locally. Good for a capstone where the files live on a shared
  Drive/WhatsApp and don't need to travel through git.
- **Option B (if you want them versioned in the repo):** use
  [Git LFS](https://git-lfs.github.com) for these specific files:
  ```bash
  git lfs install
  git lfs track "*.pth" "Music_dataset2.csv"
  git add .gitattributes Music_dataset2.csv metadata2.pth rnn_model_trained2.pth ncf_model_trained2.pth
  git commit -m "Add dataset and trained models via Git LFS"
  git push
  ```
  (Then remove the four filenames from `.gitignore` first, or `git add -f` them.)

**If you deploy on Streamlit Community Cloud:**
1. Push the repo as above.
2. On [share.streamlit.io](https://share.streamlit.io), "New app" → pick
   your repo → branch `main` → main file path `app.py`.
3. In the app's **Settings → Secrets**, paste the contents of
   `.streamlit/secrets.toml.example` with your real values filled in
   (or leave them blank to stay in fallback mode).
4. If you used Option A above for the large files, Streamlit Cloud won't
   have them either — use Option B (Git LFS) for a cloud deployment, or
   accept that the deployed version runs in demo/content-based-fallback
   mode (which is genuinely fine for a panel demo).

## 5. To use real data/models instead of fallbacks (local machine)

- **MongoDB:** put `MONGO_URI` in `.streamlit/secrets.toml` (see `.env.example`).
- **OTP email login:** put `BREVO_API_KEY`, `SENDER_EMAIL`, `HOST_EMAILS`.
- **Real song catalog:** place `Music_dataset2.csv` in the project root
  (same columns the original app expected: song/track, artist, genre,
  valence, energy, tempo, release date).
- **Trained RNN/NCF models:** place `metadata2.pth`, `rnn_model_trained2.pth`,
  `ncf_model_trained2.pth` in the project root.
- **WESAD (physiological research dataset):** register and download from
  the official source, then place each subject at
  `data/wesad/S<id>/S<id>.pkl` (official per-subject pickle format).
  **This project does not include WESAD and cannot auto-download it.**

## 6. Dataset traceability

| Dataset | Purpose | Variables used | Source | Status in this repo |
|---|---|---|---|---|
| WESAD | Physiological stress signals, HRV pipeline design | ECG (chest, 700Hz) → RR intervals → HRV features | Schmidt et al., 2018, ICMI, doi:10.1145/3242969.3242985 | **Not included** — interface built, awaiting your download |
| PMEmo | Song-level emotion + EDA | Referenced for evidence mapping only, not integrated as training data in this build | Zhang et al., 2018, ACM ICMR, doi:10.1145/3206025.3206037 | Referenced, not integrated |
| DEAP | Music-video physiological affect | Referenced for evidence mapping only | Koelstra et al., 2012, IEEE TAC, doi:10.1109/T-AFFC.2011.15 | Referenced, not integrated |

DEAM was not integrated in this build (no audio-emotion-label training
pipeline was added — the existing RNN/NCF models are unchanged). If you
want DEAM-driven audio-feature/emotion labeling, that's a clearly separable
next phase — say so and it can be built next.

## 7. Research evidence used (verify DOIs independently before citing formally)

- Gomez, P., & Danuser, B. (2007). *Relationships between musical structure
  and psychophysiological measures of emotion.* Emotion, 7(2), 377-387.
  doi:10.1037/1528-3542.7.2.377
- Trappe, H. J. (2010). *The effects of music on the cardiovascular system
  and cardiovascular health.* Heart, 96(23), 1868-1871. doi:10.1136/hrt.2010.209858
- Russell, J. A. (1980). *A circumplex model of affect.* Journal of
  Personality and Social Psychology, 39(6), 1161-1178. doi:10.1037/h0077714
- Gosling, S. D., Rentfrow, P. J., & Swann, W. B. (2003). *A very brief
  measure of the Big-Five personality domains.* Journal of Research in
  Personality, 37(6), 504-528. doi:10.1016/S0092-6566(03)00046-1
- Lovibond, S. H., & Lovibond, P. F. (1995). *Manual for the Depression
  Anxiety Stress Scales* (2nd ed.). Psychology Foundation of Australia.
- The WHOQOL Group (1998). *Development of the WHOQOL-BREF quality of life
  assessment.* Psychological Medicine, 28(3), 551-558. doi:10.1017/S0033291798006667
- Shaffer, F., & Ginsberg, J. P. (2017). *An overview of heart rate
  variability metrics and norms.* Frontiers in Public Health, 5, 258.
  doi:10.3389/fpubh.2017.00258

Full details, claim-level distinctions (song vs. characteristic vs. genre vs.
general relationship), and limitations are in the app's **Research Evidence**
page and `modules/evidence.py`.

## 8. Known limitations (state these to your panel — don't let them ask first)

- HR/stress on the **Physiological Input → Self-report** tab are
  self-reported sliders, not sensor measurements — they feed the
  recommendation engine exactly as the original app did.
- Real HRV is only computed when you upload an actual RR-interval file or
  process a WESAD subject — never fabricated.
- WESAD, PMEmo and DEAP are not merged. They measure different things
  (see the Dataset/Research Mode page) and merging them without a
  justified mapping would misrepresent the data.
- The R-peak detector in `physio.wesad_ecg_to_rr` is a minimal
  Pan-Tompkins-style implementation for demonstrating the raw-ECG → RR →
  HRV pipeline; a submitted research analysis should use a validated
  library (e.g. NeuroKit2) instead.
- Validation metrics (correlation, Precision@K) only appear once enough
  real feedback rows exist (gated in `modules/validation.py`) — before
  that, the app says so explicitly rather than showing a number.
- The Bias page is a structured checklist you fill in, not an
  auto-computed "bias score" — there is no such thing as an
  automatically-objective bias score for a system like this.
- The evidence base cites music-*characteristic* and genre-*trend*
  research; it does **not** claim any specific catalog song has been
  clinically tested.

## 9. Panel-defense quick answers

- **Why HRV?** Time-domain HRV features (SDNN/RMSSD/pNN50) are standard,
  literature-defined autonomic-nervous-system indicators (Shaffer &
  Ginsberg, 2017); we compute them only from real RR-interval data.
- **Why WESAD?** It's the standard public benchmark for wearable
  stress/affect detection with labeled physiological signals (Schmidt et
  al., 2018) — appropriate for HRV/stress feature-extraction research,
  though it's lab-collected from 15 subjects, which limits generalization.
- **Why PMEmo/DEAP but not integrated?** Both connect music to
  physiological response, but at different signal types (EDA vs. video
  stimuli) than WESAD's audio-free stress protocol — arbitrarily merging
  them with WESAD or with this song catalog would misrepresent what each
  dataset actually measured, so they're documented as evidence sources,
  not merged training data.
- **Is it adaptive?** Yes — concretely: (1) the Q-tables update after every
  rating, (2) the fusion weights re-fit via Ridge regression once ≥20
  feedback rows exist, (3) songs flagged as adverse responses are
  deprioritized in future sessions.
- **What happens if a recommendation is wrong?** The safety layer
  (`modules/safety.py`) flags ratings ≤2 given during an already
  elevated-stress/low-mood state as "adverse," excludes that song from
  future pools for that user, and low-confidence score spreads trigger a
  fallback to a neutral candidate pool instead of a possibly-noisy top pick.
