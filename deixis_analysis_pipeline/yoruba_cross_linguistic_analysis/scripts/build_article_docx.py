#!/usr/bin/env python3
"""Build an enhanced Word .docx of the Yoruba deixis article:
original text (extracted) + abstract + embedded figures + worked examples + discussion.
"""
from __future__ import annotations
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parents[1]
VIZ = ROOT / "visualizations_open"
SRC = Path(r"C:\dev\deixis\_articleYoruba_extracted.txt")
OUT = ROOT / "Article_Yoruba_Deixis_Enhanced.docx"

# figure -> (filename, caption) inserted AFTER the numbered result section key
FIGS = {
    "1.": ("41_macro_markers_en_vs_yo.png",
           "Figure 1. Yoruba commands, English explains. Direct imperatives, pronoun density, and "
           "obligation density are roughly 2x higher in Yoruba; hedging is higher in English "
           "(GPT-4o + Claude). The imperative gap (3% vs 65%) is version-clean (holds for GPT-4o)."),
    "4.": ("40_deixis_decision_summary.png",
           "Figure 2. How deixis and language shape the decision and the ethic. A: ethical approach by "
           "language. B: commit rate by framing. C: share of cells where the decision flips English->Yoruba, "
           "by dilemma. D: framing x ethic (descriptive; not significant)."),
    "6.": ("42_emphatic_committed_vs_hedged.png",
           "Figure 3. Emphatic emi is elevated where the model commits. Corrected emphatic ratio "
           "emi/(mo+emi) is higher in committed than hedged Yoruba responses (0.22 vs 0.13, "
           "Mann-Whitney p = 0.022)."),
    "7.": ("16_mi_emi_mo_four_model_framing.png",
           "Figure 4. mo / emi / mi per 100 words by framing, four models (open Yoruba). Claude leans on "
           "emphatic emi; DeepSeek and N-ATLaS are strongly mo-dominant."),
    "8.": ("26_natlas_open_vs_cloud_summary.png",
           "Figure 5. Open four-model summary. Length, mo vs emi, corrected emphatic ratio, language "
           "stability, deictic uptake, and genre. The native N-ATLaS is most mo-dominant and least "
           "emphatic, yet commits readily."),
    "9.": ("31_genre_by_model.png",
           "Figure 6. Response genre by model (open Yoruba). Cloud models concentrate in balanced "
           "exposition; N-ATLaS is the only model with a genuine genre spread."),
    "13.": ("25_emphatic_ratio_raw_vs_corrected.png",
            "Figure 7. Emphatic ratio: raw vs corrected for the emi/e-mi (life) homograph. The correction "
            "is largest for Claude (43 e-mi-as-life tokens)."),
}
SECOND_FIG_13 = ("23_emi_emphatic_vs_emi_life_by_dilemma.png",
                 "Figure 8. emi (emphatic 'I') vs e-mi ('life'), by dilemma and model. Solid = emphatic; "
                 "hatched = life. Claude's trolley bar is almost entirely 'life'.")

ABSTRACT = (
    "This article presents a cross-linguistic analysis of deictic framing and moral reasoning in large "
    "language models across English and Yoruba, using four models: OpenAI (gpt-4o), Anthropic (Claude), "
    "DeepSeek, and the Yoruba/Nigeria-native model N-ATLaS. The corpus is recoded into a shared "
    "discourse-analytic schema across six ethical dilemmas and nine deictic framings, with the Yoruba "
    "first-person forms mo, emi, and mi disambiguated from the tonal homograph e-mi ('life'). The clearest "
    "result is a language effect rather than a frame-by-framework mapping. Relative to English, Yoruba "
    "responses commit far more often (refuse-to-commit 14% vs 30%, p = 0.005) and are far more ethically "
    "differentiated (53% take a named stance vs 17%, p < 0.001); the shift is grammatically concrete and "
    "version-clean (Yoruba is ~2x more pronoun-dense and far more imperative, 65% vs 3%, p < 0.001, in both "
    "GPT-4o and Claude). Switching language flips the coded decision in ~45% of matched cells, while frame "
    "uptake itself is identical across languages (indexical coherence 0.90 vs 0.91). The central linguistic "
    "finding is that Yoruba's mo/emi contrast gives models a grammatical lever for moral commitment that "
    "English's single 'I' lacks: emphatic emi is elevated where a model avows a stance (0.22 vs 0.13, "
    "p = 0.022). Yet models inhabit the resource differently (corrected emphatic ratio: Claude 0.32 > "
    "GPT-4o 0.18 > DeepSeek 0.07 ~ N-ATLaS 0.07), and the native N-ATLaS inverts the cloud pattern - most "
    "mo-dominant, least emphatic, committing through mo plus decision verbs. Moral stance in multilingual "
    "LLMs is therefore not a language-invariant model trait but is partly constituted by language-specific "
    "deictic morphology that English flattens and no single model realizes uniformly."
)

EXAMPLES_HEADING = "Worked example: one dilemma, five frames, five ethics"
EXAMPLES = [
    ("Claude, Yoruba, whistleblower dilemma - all five framings reach 'disclose', each via a different "
     "ethics, showing that the deictic frame re-selects the moral idiom:"),
    ("- impersonal -> duty/right-to-know: \"Osise naa ye ki o safihan...\" (the employee should disclose).",),
    ("- second person -> utilitarian, with emphatic emi: \"Emi yoo safihan... emi eniyan ko ni iye owo\" "
     "(\"I myself will disclose... a human life has no price\").",),
    ("- reflexive -> hesitation: \"first explore talking to your colleague...\".",),
    ("- spatial -> procedural: a numbered protocol (protect outsiders -> talk to colleague -> seek help).",),
    ("- cosmological -> virtue: trust and integrity above friendship, money, job.",),
    ("Cross-language flip (Claude, whistleblower, cosmological): English stays conditional - \"I aim to "
     "explore this carefully..., I'd encourage...\" - while Yoruba commits: \"Ohun ti o gbodo se ni lati "
     "safihan... Emi awon eniyan se pataki ju gbogbo nnkan lo\" (\"What you must do is disclose... people's "
     "lives matter more than anything\"). Same model, dilemma, and frame; the language changes the verdict."),
]

DISCUSSION = [
    ("Discussion: a linguistic mechanism, model-specific calibration", 1),
    ("These findings support a precise, linguistically grounded claim: moral stance in multilingual LLMs "
     "is partly constituted by the deictic morphology of the output language. The deictic mechanism itself "
     "is language-invariant - across all four model families, frame uptake is strong and the assigned moral "
     "agent is stable (indexical coherence 0.90 English / 0.91 Yoruba). What diverges is the content: Yoruba "
     "fills the same deictic structures with more imperatives, stronger obligation, denser person-marking, "
     "and more differentiated ethics. A cross-family consistency test makes the split explicit: properties "
     "that recur across families (frame uptake; use of the mo/emi/e-mi system) point to a genuine linguistic "
     "mechanism, while properties that diverge (emphatic magnitude, genre, dilemma-placement) are "
     "model-specific - driven by training register, alignment, and decoding rather than architecture.", 0),
    ("The mo/emi contrast maps onto a Yoruba distinction between ironu (reflection) and ipinnu (decision): "
     "mo ro pe... opens deliberative space; emi yoo... closes it into avowed decision. The models reproduce "
     "this calibration, but unevenly. Claude dramatizes the emphatic self (amplified by its tendency to dwell "
     "on e-mi, 'life', in existential dilemmas); the native model performs ownership through mo plus decision "
     "verbs and distributes responsibility relationally. The contribution is therefore not 'emphatic emi is "
     "the authentic Yoruba marker of commitment' - the native model refutes that - but 'the mo/emi contrast "
     "is a commitment-calibration resource that models inhabit in language- and model-specific ways'.", 0),
    ("Implications for multilingual alignment", 1),
    ("If a model's moral commitment, decisiveness, and ethical idiom change with the language of the prompt - "
     "and the coded decision itself flips in ~45% of matched cells - then alignment evaluated only in English "
     "does not straightforwardly transfer. Yoruba elicits a more directive, obligation-bearing, verdict-like "
     "moral voice from the same systems. For deployment in Yoruba-speaking contexts this is double-edged: more "
     "decisiveness can be more useful or more risky, and the shift is partly an artifact of training and "
     "alignment history rather than a considered design choice. Evaluations of moral and safety behavior "
     "should therefore be run in the deployment language, not assumed from English.", 0),
    ("Originality and limitations", 1),
    ("The study's originality lies in treating deixis as a moral-positioning device and in using a "
     "language - Yoruba - whose grammar makes moral self-involvement visible where English flattens it to a "
     "single 'I'; in a tonal disambiguation (emi vs e-mi) that prevents 'life' from being miscounted as "
     "selfhood; and in a native-model control (N-ATLaS) that separates Yoruba linguistic affordances from the "
     "way Western cloud models inhabit them. Limitations bound the claims: the cross-language coded corpus "
     "centers on GPT-4o and Claude; Claude's Yoruba runs used Claude Sonnet 4 while its English runs used "
     "Claude 3.5 Sonnet (a version confound, so version-clean claims rest on GPT-4o); per-frame cells are "
     "small (N <= 12), so the framing->ethic mapping is a hypothesis, not a result; and tone-mark "
     "disambiguation, while conservative, is imperfect.", 0),
    ("Conclusion", 1),
    ("Yoruba's mo/emi contrast gives multilingual LLMs a grammatical lever for moral commitment that English "
     "lacks, and the models pull it: emphatic emi is elevated where they avow a stance (p = 0.022), and Yoruba "
     "moral discourse is, at scale, more pronoun-marked, more imperative, and less hedged than its English "
     "counterpart - while the underlying frame uptake is identical across languages. Yet each model family "
     "inhabits the resource differently, and the native model commits through mo, not emi. Moral stance, in "
     "these systems, is neither a fixed model trait nor a universal of 'Yoruba', but an interaction: a "
     "language-specific deictic grammar, recruited model-specifically, to stage who owns the moral decision.", 0),
]


def is_results_heading(t):
    return t[:3] in {f"{i}.": None for i in range(1, 15)} or (t[:2].rstrip(".").isdigit() and t[1:3] in (". ", "."))


def main():
    paras = [p.strip() for p in SRC.read_text(encoding="utf-8").split("\n\n") if p.strip()]
    doc = Document()
    # title
    h = doc.add_heading("The Grammar of Moral Commitment: Deixis, mo / emi, and Moral Reasoning "
                        "in Multilingual LLMs (English and Yoruba)", level=0)
    # abstract
    doc.add_heading("Abstract", level=1)
    ap = doc.add_paragraph(); r = ap.add_run(ABSTRACT); r.italic = True

    top = {"Introduction", "Methodology", "Results"}
    num_keys = [f"{i}." for i in range(1, 15)]

    for p in paras:
        if p in top:
            doc.add_heading(p, level=1)
            continue
        key = next((k for k in num_keys if p.startswith(k)), None)
        if key:
            doc.add_heading(p, level=2)
            continue
        doc.add_paragraph(p)
        # after the body text of a numbered section, insert its figure(s)
        # (we track last numbered key seen)
    # Re-run with figure injection (simpler: rebuild linearly tracking section)
    # --- rebuild properly ---
    doc2 = Document()
    doc2.add_heading("The Grammar of Moral Commitment: Deixis, mo / emi, and Moral Reasoning "
                     "in Multilingual LLMs (English and Yoruba)", level=0)
    doc2.add_heading("Abstract", level=1)
    ap = doc2.add_paragraph(); r = ap.add_run(ABSTRACT); r.italic = True

    cur = None
    fig_done = set()
    def add_fig(fname, cap):
        img = VIZ / fname
        if img.exists():
            doc2.add_picture(str(img), width=Inches(6.2))
            doc2.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp = doc2.add_paragraph(); cr = cp.add_run(cap); cr.italic = True; cr.font.size = Pt(9)

    for p in paras:
        if p in top:
            doc2.add_heading(p, level=1); cur = None; continue
        key = next((k for k in num_keys if p.startswith(k)), None)
        if key:
            doc2.add_heading(p, level=2); cur = key; continue
        doc2.add_paragraph(p)
        # inject figure once, right after first body para of the mapped section
        if cur in FIGS and cur not in fig_done:
            fn, cap = FIGS[cur]; add_fig(fn, cap); fig_done.add(cur)
            if cur == "13.":
                add_fig(*SECOND_FIG_13)
            if cur == "6.":
                # worked examples block after fig 3
                doc2.add_heading(EXAMPLES_HEADING, level=2)
                for ex in EXAMPLES:
                    doc2.add_paragraph(ex[0])
    # discussion etc.
    for text, lvl in DISCUSSION:
        if lvl == 1:
            doc2.add_heading(text, level=1)
        else:
            doc2.add_paragraph(text)

    doc2.save(str(OUT))
    print("Saved", OUT, "| paragraphs in source:", len(paras), "| figures inserted:", len(fig_done) + 1)


if __name__ == "__main__":
    main()
