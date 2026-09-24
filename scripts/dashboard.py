#!/usr/bin/env python3
"""Dashboard do experimento: página HTML única + figuras SVG/PNG.

Lê os dados com dataset.load() e compara os tratamentos nas três RQs:
tempo até verde (RQ1), sucesso e testes falhando (RQ2) e métricas estruturais
(RQ3). Os gráficos são desenhados com Matplotlib/Seaborn; o SVG é embutido na
página com as cores trocadas por variáveis CSS, o que dá modo claro/escuro sem
redesenhar. Os PNGs (tema claro) servem para o relatório.

Apenas descreve os dados: testes estatísticos ficam em outros scripts.
"""
import argparse
from datetime import datetime, timezone
import html
from io import StringIO
from pathlib import Path
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import numpy as np  # noqa: E402
import seaborn as sns  # noqa: E402

from dataset import load  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "doc/dashboard"

TREATMENTS = ["sem-ia", "com-ia"]
LABELS = {"sem-ia": "Sem IA", "com-ia": "Com IA"}
KATAS_PER_TREATMENT = 3  # desenho contrabalanceado: 6 katas, metade em cada tratamento
FIGURES = ["tempo_distribuicao", "tempo_participante", "tempo_kata", "estrutura"]

# Cores do tema claro (validadas para daltonismo) e a variável CSS que as substitui
# no SVG embutido. O modo escuro redefine só as variáveis.
THEME = {
    "#eb6834": "--sem-ia",
    "#2a78d6": "--com-ia",
    "#0b0b0b": "--ink",
    "#52514e": "--ink-2",
    "#898781": "--muted",
    "#e1e0d9": "--grid",
    "#c3c2b7": "--axis",
    "#fcfcfb": "--surface",
}
COLOR = {"sem-ia": "#eb6834", "com-ia": "#2a78d6"}
INK, INK_2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SURFACE = "#fcfcfb"

STRUCTURE = [
    ("complexity_avg", "Complexidade ciclomática média/método"),
    ("loc_total", "LOC"),
    ("duplication_percent", "Duplicação (%)"),
]


def fmt(value, digits=1):
    if value is None or value != value:
        return "–"
    return f"{value:.{digits}f}".replace(".", ",")


def completed(df):
    return df[df["status"] == "completed"]


def summary(df):
    """Números de destaque por tratamento; tempo só sobre trials concluídos."""
    by = {}
    for t in TREATMENTS:
        part = df[df["treatment"] == t]
        done = completed(part)
        by[t] = {
            "n": len(part),
            "median_minutes": float(done["time_to_green_minutes"].median())
            if len(done)
            else float("nan"),
            "success_rate": 100.0 * len(done) / len(part) if len(part) else float("nan"),
            "failed": int(part["failed"].fillna(0).sum()),
            "complexity": float(part["complexity_avg"].median()),
        }
    sem, com = by["sem-ia"]["median_minutes"], by["com-ia"]["median_minutes"]
    return {
        "n": len(df),
        "expected": df["participant"].nunique() * KATAS_PER_TREATMENT * 2,
        "by_treatment": by,
        "censored": int(df["censored"].sum()),
        "speedup": sem / com if com else float("nan"),
    }


def missing_pairs(df):
    """Participantes sem nenhum trial em algum tratamento."""
    gaps = []
    for participant, part in df.groupby("participant"):
        for t in TREATMENTS:
            if not (part["treatment"] == t).any():
                gaps.append((participant, t))
    return gaps


# ---------------------------------------------------------------- figuras


def style():
    sns.set_theme(style="white", rc={"axes.facecolor": "none"})
    plt.rcParams.update(
        {
            "svg.fonttype": "none",
            "svg.hashsalt": "lab02",
            "font.family": "sans-serif",
            "font.size": 9,
            "text.color": INK,
            "axes.labelcolor": INK_2,
            "axes.edgecolor": AXIS,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.6,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelcolor": INK_2,
            "ytick.labelcolor": INK_2,
            "figure.facecolor": "none",
            "legend.frameon": False,
        }
    )


def br_ticks(ax):
    """Separador decimal brasileiro e sem casas desnecessárias nos eixos."""
    formatter = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
    for axis in (ax.xaxis, ax.yaxis):
        if isinstance(axis.get_major_formatter(), matplotlib.ticker.ScalarFormatter):
            axis.set_major_formatter(formatter)


def jitter(n, spread=0.28):
    return np.array([((i * 0.618) % 1 - 0.5) * spread for i in range(n)])


def tooltip(r):
    parts = [f"{r.participant} · {r.kata} · {LABELS[r.treatment]}"]
    if r.status == "completed":
        parts.append(f"{fmt(r.time_to_green_minutes)} min até verde")
    else:
        parts.append(r.status)
    return "\n".join(parts)


def point(ax, x, y, treatment, gid, tips, title, hollow=False, size=46):
    color = COLOR[treatment]
    ax.scatter(
        [x],
        [y],
        s=size,
        color="none" if hollow else color,
        edgecolor=color if hollow else SURFACE,
        linewidth=1.4 if hollow else 1.2,
        zorder=3,
        gid=gid,
    )
    tips[gid] = title


def fig_tempo_distribuicao(df, tips):
    fig, ax = plt.subplots(figsize=(8, 2.6))
    done = completed(df)
    rows = {"sem-ia": 1, "com-ia": 0}
    sns.boxplot(
        data=done,
        x="time_to_green_minutes",
        y=done["treatment"].map(rows),
        orient="h",
        order=[0, 1],
        width=0.42,
        fill=False,
        showfliers=False,
        linewidth=1.1,
        color=AXIS,
        medianprops={"color": INK, "linewidth": 2},
        ax=ax,
    )
    limit = df["limit_seconds"].max() / 60 if len(df) else 35
    for t, y in rows.items():
        part = df[df["treatment"] == t].reset_index(drop=True)
        offsets = jitter(len(part))
        for i, r in enumerate(part.itertuples()):
            censored = r.status != "completed"
            x = limit if censored else r.time_to_green_minutes
            point(ax, x, y + offsets[i], t, f"dist-{r.trial_id}", tips, tooltip(r), hollow=censored)
    ax.set_yticks([0, 1], [LABELS["com-ia"], LABELS["sem-ia"]])
    ax.set_ylabel("")
    ax.set_xlabel("minutos até todos os testes passarem")
    ax.set_xlim(left=0)
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=10)
    fig.tight_layout()
    return fig


def spread_labels(ys, gap):
    """Afasta rótulos verticais que colidiriam, preservando a ordem."""
    order = np.argsort(ys)
    placed = list(ys)
    for a, b in zip(order, order[1:]):
        if placed[b] - placed[a] < gap:
            placed[b] = placed[a] + gap
    return placed


def fig_tempo_participante(df, tips):
    fig, ax = plt.subplots(figsize=(8, 3.8))
    done = completed(df)
    medians = done.groupby(["participant", "treatment"], observed=True)[
        "time_to_green_minutes"
    ].median()
    xs = {"sem-ia": 0, "com-ia": 1}
    top = float(medians.max()) if len(medians) else 1
    labels = []
    for participant in sorted(df["participant"].unique()):
        values = {t: medians.get((participant, t)) for t in TREATMENTS}
        present = {t: v for t, v in values.items() if v is not None and v == v}
        if len(present) == 2:
            ax.plot([0, 1], [present["sem-ia"], present["com-ia"]], color=AXIS, lw=2, zorder=2)
            ratio = present["sem-ia"] / present["com-ia"]
            note = f"{fmt(ratio)}× mais rápido" if ratio >= 1 else f"{fmt(1 / ratio)}× mais lento"
            labels.append((present["com-ia"], f"{participant} · {note}", INK))
        elif present:
            only = next(iter(present))
            labels.append((present[only], f"{participant} · só {LABELS[only][0].lower() + LABELS[only][1:]}, sem par", MUTED))
        for t, v in present.items():
            title = f"{participant} · {LABELS[t]}\nmediana {fmt(v)} min"
            point(ax, xs[t], v, t, f"part-{participant}-{t}", tips, title, size=70)
    placed = spread_labels([y for y, _, _ in labels], top * 0.07)
    for (_, text, color), y in zip(labels, placed):
        ax.text(1.08, y, text, va="center", fontsize=9, color=color)
    ax.set_xticks([0, 1], [LABELS["sem-ia"], LABELS["com-ia"]])
    ax.tick_params(axis="x", length=0, labelsize=10)
    ax.set_xlim(-0.25, 2.1)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("mediana de minutos até verde")
    ax.grid(axis="x", visible=False)
    ax.spines["bottom"].set_visible(False)
    fig.tight_layout()
    return fig


def dumbbell(ax, df, column, tips, prefix):
    katas = sorted(df["kata"].unique())
    rows = {k: len(katas) - 1 - i for i, k in enumerate(katas)}
    for kata, y in rows.items():
        part = df[df["kata"] == kata]
        meds = part.groupby("treatment", observed=True)[column].median().dropna()
        if len(meds) == 2:
            ax.plot(meds.values, [y, y], color=AXIS, lw=3, solid_capstyle="round", zorder=1)
        for t, median in meds.items():
            ax.plot([median, median], [y - 0.22, y + 0.22], color=COLOR[t], lw=2, zorder=2)
        for t in TREATMENTS:
            for r in part[part["treatment"] == t].itertuples():
                value = getattr(r, column)
                if value != value:
                    continue
                title = f"{r.participant} · {r.kata} · {LABELS[t]}\n{fmt(value, 2)}"
                point(ax, value, y, t, f"{prefix}-{r.trial_id}", tips, title)
    ax.set_yticks(list(rows.values()), list(rows.keys()))
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    ax.set_ylim(-0.6, len(katas) - 0.4)


def legend(fig):
    handles = [
        plt.Line2D([], [], marker="o", ls="", markersize=7, color=COLOR[t], label=LABELS[t])
        for t in TREATMENTS
    ]
    fig.legend(handles=handles, loc="upper left", ncol=2, bbox_to_anchor=(0.01, 1.0),
               labelcolor=INK_2, handletextpad=0.3, columnspacing=1.2)


def fig_tempo_kata(df, tips):
    fig, ax = plt.subplots(figsize=(8, 3.6))
    dumbbell(ax, completed(df), "time_to_green_minutes", tips, "kata")
    ax.set_xlim(left=0)
    ax.set_xlabel("minutos até verde")
    legend(fig)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    return fig


def structure_panels(df):
    return [(c, label) for c, label in STRUCTURE if df[c].fillna(0).abs().sum() > 0]


def fig_estrutura(df, tips):
    panels = structure_panels(df) or STRUCTURE[:1]
    fig, axes = plt.subplots(1, len(panels), figsize=(4.2 * len(panels), 3.6), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, (column, label) in zip(axes, panels):
        dumbbell(ax, df, column, tips, f"est-{column}")
        ax.set_xlabel(label)
        ax.set_xlim(left=0)
    legend(fig)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return fig


def fig_rq2(df, tips):
    """Só desenhada quando há diferença a mostrar (algum censurado ou falha)."""
    fig, ax = plt.subplots(figsize=(8, 2.2))
    rows = {"sem-ia": 1, "com-ia": 0}
    for t, y in rows.items():
        part = df[df["treatment"] == t].reset_index(drop=True)
        offsets = jitter(len(part))
        for i, r in enumerate(part.itertuples()):
            title = f"{r.participant} · {r.kata} · {LABELS[t]}\n{int(r.failed or 0)} testes falhando"
            point(ax, r.failed or 0, y + offsets[i], t, f"rq2-{r.trial_id}", tips, title)
    ax.set_yticks([0, 1], [LABELS["com-ia"], LABELS["sem-ia"]])
    ax.set_xlabel("testes falhando na avaliação final")
    ax.set_xlim(left=-0.3)
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=10)
    fig.tight_layout()
    return fig


def themed_svg(raw, name, tips, label):
    """SVG do Matplotlib -> SVG embutível: responsivo, cores por variável, tooltips."""
    svg = raw[raw.index("<svg"):]
    svg = svg.replace(
        "<svg", f'<svg class="chart" role="img" aria-label="{html.escape(label)}"', 1
    )
    for hexcode, var in THEME.items():
        svg = re.sub(re.escape(hexcode), f"var({var})", svg, flags=re.IGNORECASE)
    for gid, title in tips.items():
        svg = svg.replace(
            f'<g id="{gid}">',
            f'<g id="{name}-{gid}" class="pt"><title>{html.escape(title)}</title>',
            1,
        )
    return svg


def render(fig, out, name, tips, label):
    for ax in fig.axes:
        br_ticks(ax)
    fig.savefig(out / f"{name}.png", dpi=200, facecolor=SURFACE)
    buffer = StringIO()
    fig.savefig(buffer, format="svg", metadata={"Date": None})
    plt.close(fig)
    raw = buffer.getvalue()
    (out / f"{name}.svg").write_text(raw, encoding="utf-8")
    return themed_svg(raw, name, tips, label)


# ---------------------------------------------------------------- página


def tile(label, value, detail=""):
    return (
        f'<div class="tile"><div class="tile-label">{label}</div>'
        f'<div class="tile-value">{value}</div><div class="tile-detail">{detail}</div></div>'
    )


def table(df):
    cols = [
        ("participant", "Participante", None),
        ("kata", "Kata", None),
        ("treatment", "Tratamento", None),
        ("status", "Estado", None),
        ("time_to_green_minutes", "Min. até verde", 1),
        ("failed", "Falhando", 0),
        ("loc_total", "LOC", 0),
        ("complexity_avg", "Complex. média", 2),
        ("duplication_percent", "Dupl. %", 1),
    ]
    head = "".join(
        f'<th{" class=num" if d is not None else ""}>{label}</th>' for _, label, d in cols
    )
    body = []
    for r in df.sort_values(["participant", "kata"]).itertuples():
        cells = []
        for c, _, digits in cols:
            v = getattr(r, c)
            if digits is None:
                text = LABELS.get(v, v) if c == "treatment" else v
                cells.append(f"<td>{html.escape(str(text))}</td>")
            else:
                cells.append(f'<td class="num">{fmt(v, digits)}</td>')
        body.append(f'<tr title="{html.escape(r.trial_id)}">{"".join(cells)}</tr>')
    return f'<table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def notes(df):
    items = []
    for participant, t in missing_pairs(df):
        items.append(
            f"<li><strong>{html.escape(participant)}</strong> ainda não tem trials "
            f"<strong>{LABELS[t]}</strong>: fica sem par nas comparações por participante.</li>"
        )
    no_metrics = df[~df["has_metrics"]]["trial_id"].tolist()
    if no_metrics:
        items.append(
            "<li>Trials sem <code>metrics.json</code> (fora da RQ3): "
            + ", ".join(html.escape(t) for t in no_metrics)
            + ".</li>"
        )
    if not items:
        return ""
    return f'<aside class="notes"><h3>Dados incompletos</h3><ul>{"".join(items)}</ul></aside>'


def build(df, out=DEFAULT_OUT):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    style()
    s = summary(df)
    sem, com = s["by_treatment"]["sem-ia"], s["by_treatment"]["com-ia"]

    charts = {}
    specs = [
        ("tempo_distribuicao", fig_tempo_distribuicao, "Distribuição do tempo até verde por tratamento"),
        ("tempo_participante", fig_tempo_participante, "Mediana de tempo por participante, sem IA e com IA"),
        ("tempo_kata", fig_tempo_kata, "Tempo até verde por kata e tratamento"),
        ("estrutura", fig_estrutura, "Métricas estruturais por kata e tratamento"),
    ]
    show_rq2 = s["censored"] > 0 or sem["failed"] + com["failed"] > 0
    if show_rq2:
        specs.append(("rq2", fig_rq2, "Testes falhando ao final por tratamento"))
    for name, draw, label in specs:
        tips = {}
        fig = draw(df, tips)
        charts[name] = render(fig, out, name, tips, label)

    speed = s["speedup"]
    hero = (
        f"{fmt(speed)}×" if speed == speed and speed >= 1 else f"{fmt(1 / speed)}×" if speed == speed else "–"
    )
    hero_text = (
        "mais rápido com IA" if speed == speed and speed >= 1 else "mais lento com IA"
    )
    tiles = "".join(
        [
            tile("Trials analisados", f'{s["n"]}<span class="of">/{s["expected"]}</span>',
                 f'{sem["n"]} sem IA · {com["n"]} com IA'),
            tile("Mediana sem IA", f'{fmt(sem["median_minutes"])} <span class="unit">min</span>',
                 '<span class="dot sem"></span>até todos os testes passarem'),
            tile("Mediana com IA", f'{fmt(com["median_minutes"])} <span class="unit">min</span>',
                 '<span class="dot com"></span>até todos os testes passarem'),
            tile("Censurados", str(s["censored"]), "atingiram 35 min sem passar"),
        ]
    )
    rq2_tiles = "".join(
        [
            tile("Sucesso sem IA", f'{fmt(sem["success_rate"], 0)}%', f'{sem["failed"]} testes falhando no total'),
            tile("Sucesso com IA", f'{fmt(com["success_rate"], 0)}%', f'{com["failed"]} testes falhando no total'),
        ]
    )
    rq2_body = (
        charts["rq2"]
        if show_rq2
        else '<p class="empty">Todos os trials terminaram com todos os testes passando: '
        "não há diferença de defeitos a desenhar por enquanto.</p>"
    )
    skipped = [label for c, label in STRUCTURE if (c, label) not in structure_panels(df)]
    rq3_note = (
        f'<p class="empty">{", ".join(skipped)}: 0 em todos os trials (painel omitido).</p>'
        if skipped
        else ""
    )
    generated = datetime.now(timezone.utc).astimezone().strftime("%d/%m/%Y %H:%M")
    page = PAGE.format(
        hero=hero,
        hero_text=hero_text,
        tiles=tiles,
        rq2_tiles=rq2_tiles,
        rq2_body=rq2_body,
        rq3_note=rq3_note,
        rq3_complexity=f'{fmt(sem["complexity"])} → {fmt(com["complexity"])}',
        notes=notes(df),
        table=table(df),
        generated=generated,
        **charts,
    )
    (out / "index.html").write_text(page, encoding="utf-8")
    return out / "index.html"


PAGE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IA vs. Manual — Dashboard</title>
<style>
:root {{
  color-scheme: light;
  --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
  --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7;
  --border: rgba(11,11,11,0.10);
  --sem-ia: #eb6834; --com-ia: #2a78d6;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    color-scheme: dark;
    --page: #0d0d0d; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7;
    --muted: #898781; --grid: #2c2c2a; --axis: #383835;
    --border: rgba(255,255,255,0.10);
    --sem-ia: #d95926; --com-ia: #3987e5;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --page: #0d0d0d; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7;
  --muted: #898781; --grid: #2c2c2a; --axis: #383835;
  --border: rgba(255,255,255,0.10);
  --sem-ia: #d95926; --com-ia: #3987e5;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--page); color: var(--ink);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
}}
main {{ max-width: 1080px; margin: 0 auto; padding: 40px 24px 64px; }}
header {{ display: grid; grid-template-columns: 1fr auto; gap: 24px; align-items: end;
  padding-bottom: 28px; border-bottom: 1px solid var(--border); }}
.eyebrow {{ color: var(--muted); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; }}
h1 {{ font-size: clamp(28px, 4vw, 40px); line-height: 1.1; margin: 6px 0 8px; font-weight: 650; }}
.lede {{ color: var(--ink-2); margin: 0; max-width: 56ch; }}
.hero {{ text-align: right; }}
.hero-value {{ font-size: clamp(48px, 8vw, 88px); font-weight: 700; line-height: 1; letter-spacing: -.02em; }}
.hero-text {{ color: var(--ink-2); }}
.hero-text small {{ display: block; color: var(--muted); font-size: 12px; }}
.tiles {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 28px 0 8px; }}
.tiles.two {{ grid-template-columns: repeat(2, 1fr); }}
.tile {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; }}
.tile-label {{ color: var(--muted); font-size: 12px; }}
.tile-value {{ font-size: 28px; font-weight: 650; margin: 2px 0; }}
.tile-value .of, .tile-value .unit {{ color: var(--muted); font-size: 16px; font-weight: 500; }}
.tile-detail {{ color: var(--ink-2); font-size: 13px; }}
.dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }}
.dot.sem {{ background: var(--sem-ia); }} .dot.com {{ background: var(--com-ia); }}
section {{ margin-top: 48px; }}
.rq {{ color: var(--muted); font-size: 12px; font-weight: 600; letter-spacing: .08em; }}
h2 {{ font-size: 22px; margin: 4px 0 6px; font-weight: 650; }}
.question {{ color: var(--ink-2); margin: 0 0 16px; max-width: 70ch; }}
figure {{ margin: 16px 0 0; background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 16px 12px 8px; }}
figcaption {{ color: var(--ink-2); font-size: 13px; padding: 0 8px 4px; }}
figcaption strong {{ color: var(--ink); }}
svg.chart {{ max-width: 100%; height: auto; display: block; margin: 0 auto; }}
svg.chart text {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif !important; }}
svg.chart .pt {{ cursor: default; }}
svg.chart .pt:hover path, svg.chart .pt:hover use {{ stroke: var(--ink) !important; stroke-width: 2px !important; }}
.empty {{ color: var(--ink-2); background: var(--surface); border: 1px dashed var(--axis);
  border-radius: 12px; padding: 14px 16px; margin: 12px 0 0; }}
.notes {{ margin-top: 48px; border-left: 3px solid var(--sem-ia); padding: 4px 16px; }}
.notes h3 {{ font-size: 14px; margin: 0 0 4px; }}
.notes ul {{ margin: 0; padding-left: 18px; color: var(--ink-2); font-size: 14px; }}
.table-wrap {{ overflow-x: auto; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid var(--grid); white-space: nowrap; }}
th {{ color: var(--muted); font-weight: 600; }}
td.num, th.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
tbody tr:hover {{ background: var(--grid); }}
footer {{ margin-top: 40px; color: var(--muted); font-size: 12px; display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; }}
button.theme {{ font: inherit; color: var(--ink-2); background: var(--surface); border: 1px solid var(--border);
  border-radius: 999px; padding: 4px 12px; cursor: pointer; }}
@media (max-width: 760px) {{
  main {{ padding: 24px 16px 48px; }}
  header {{ grid-template-columns: 1fr; }}
  .hero {{ text-align: left; }}
  .tiles {{ grid-template-columns: repeat(2, 1fr); }}
}}
</style>
</head>
<body>
<main>
<header>
  <div>
    <div class="eyebrow">LAB02 · Experimento controlado</div>
    <h1>IA vs. codificação manual</h1>
    <p class="lede">Cada participante resolveu seis katas em Java, metade com assistente de IA e metade sem,
    em ordem contrabalanceada. Resultado de cada trial: tempo até todos os testes passarem, defeitos e estrutura do código.</p>
  </div>
  <div class="hero">
    <div class="hero-value">{hero}</div>
    <div class="hero-text">{hero_text}<small>razão entre as medianas de tempo</small></div>
  </div>
</header>

<div class="tiles">{tiles}</div>

<section>
  <div class="rq">RQ1 · TEMPO</div>
  <h2>A IA reduz o tempo para resolver a tarefa?</h2>
  <p class="question">Tempo até todos os testes passarem, em minutos. Pontos vazados são trials censurados (limite de 35 min).
  Passe o mouse sobre um ponto para ver o trial.</p>
  <figure>{tempo_distribuicao}<figcaption><strong>Distribuição.</strong> Cada ponto é um trial; a caixa mostra mediana e quartis dos concluídos.</figcaption></figure>
  <figure>{tempo_participante}<figcaption><strong>Por participante.</strong> Cada linha liga a mediana sem IA à mediana com IA da mesma pessoa.</figcaption></figure>
  <figure>{tempo_kata}<figcaption><strong>Por kata.</strong> Cada ponto é um trial; o traço colorido marca a mediana do tratamento e a barra cinza liga as duas medianas.</figcaption></figure>
</section>

<section>
  <div class="rq">RQ2 · DEFEITOS</div>
  <h2>A IA reduz a quantidade de testes falhando?</h2>
  <p class="question">Avaliação final de cada trial: proporção que terminou com todos os testes passando e total de testes falhando.</p>
  <div class="tiles two">{rq2_tiles}</div>
  {rq2_body}
</section>

<section>
  <div class="rq">RQ3 · ESTRUTURA</div>
  <h2>A IA altera a complexidade ou a duplicação do código?</h2>
  <p class="question">Métricas do PMD/CPD sobre o código final de cada trial. Mediana da complexidade média por método:
  <strong>{rq3_complexity}</strong> (sem IA → com IA).</p>
  <figure>{estrutura}<figcaption><strong>Por kata.</strong> Cada ponto é um trial; a barra liga as medianas dos tratamentos.</figcaption></figure>
  {rq3_note}
</section>

{notes}

<section>
  <div class="rq">DADOS</div>
  <h2>Todos os trials</h2>
  <div class="table-wrap">{table}</div>
</section>

<footer>
  <span>Gerado por <code>scripts/dashboard.py</code> em {generated}. Somente estatística descritiva.</span>
  <button class="theme" type="button" id="theme">Alternar tema</button>
</footer>
</main>
<script>
(function () {{
  var root = document.documentElement, key = "lab02-theme";
  try {{ var saved = localStorage.getItem(key); if (saved) root.dataset.theme = saved; }} catch (e) {{}}
  document.getElementById("theme").addEventListener("click", function () {{
    var dark = root.dataset.theme ? root.dataset.theme === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try {{ localStorage.setItem(key, root.dataset.theme); }} catch (e) {{}}
  }});
}})();
</script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "results/consolidado.csv")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    path = build(load(args.input), args.output)
    print(f"Dashboard gravado em {path}")


if __name__ == "__main__":
    main()
