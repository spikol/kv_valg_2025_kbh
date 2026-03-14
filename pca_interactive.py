# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "scikit-learn",
#   "plotly",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    import plotly.graph_objects as go

    return PCA, StandardScaler, go, mo, pd


@app.cell(hide_code=True)
def _(PCA, StandardScaler, pd):
    df_raw = pd.read_csv("https://raw.githubusercontent.com/spikol/kv_valg_2025_kbh/main/folk_version_03/combined_wide.csv")
    cols = ["candidate_id", "name", "party_code"] + [f"q{i}_answer_value" for i in range(1, 26)]
    df = df_raw[cols].dropna().copy()
    q_cols = [f"q{i}_answer_value" for i in range(1, 26)]
    q_text = {f"q{i}": df_raw[f"q{i}_question"].iloc[0] for i in range(1, 26)}

    PARTY_COLORS = {
        "A": "#E3001B", "B": "#733B80", "C": "#006437", "F": "#F04E23",
        "H": "#B5C400", "I": "#00AEEF", "M": "#00827F", "O": "#F5A623",
        "V": "#002883", "X": "#888888", "Æ": "#8B1A1A", "Ø": "#C0392B", "Å": "#2ECC71",
    }

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[q_cols])
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)
    coords[:, 0] *= -1

    df = df.copy()
    df["pc1"] = coords[:, 0]
    df["pc2"] = coords[:, 1]
    df["color"] = df["party_code"].map(lambda p: PARTY_COLORS.get(p, "#888888"))

    party_means = df.groupby("party_code")[["pc1", "pc2"]].mean().reset_index()
    party_means["color"] = party_means["party_code"].map(lambda p: PARTY_COLORS.get(p, "#888888"))

    var1 = pca.explained_variance_ratio_[0]
    var2 = pca.explained_variance_ratio_[1]
    return PARTY_COLORS, df, df_raw, party_means, q_text, var1, var2


@app.cell(hide_code=True)
def _(df, go, mo, party_means, var1, var2):
    # --- Cell 1: Full PCA — click a dot to see candidate info ---

    traces = []

    for party, group in df.groupby("party_code"):
        color = group["color"].iloc[0]
        mean_row = party_means[party_means["party_code"] == party].iloc[0]

        # Lines to party mean
        line_x, line_y = [], []
        for _, row in group.iterrows():
            line_x += [row["pc1"], mean_row["pc1"], None]
            line_y += [row["pc2"], mean_row["pc2"], None]

        traces.append(go.Scatter(
            x=line_x, y=line_y,
            mode="lines",
            line=dict(color=color, width=0.5),
            opacity=0.2,
            showlegend=False,
            hoverinfo="skip",
        ))

        # Candidate dots
        traces.append(go.Scatter(
            x=group["pc1"], y=group["pc2"],
            mode="markers",
            name=party,
            marker=dict(color=color, size=6, opacity=0.6),
            customdata=group[["name", "party_code", "candidate_id"]].values,
            hovertemplate="<b>%{customdata[0]}</b><br>Parti: %{customdata[1]}<extra></extra>",
        ))

    # Party mean dots + labels
    traces.append(go.Scatter(
        x=party_means["pc1"], y=party_means["pc2"],
        mode="markers+text",
        text=party_means["party_code"],
        textposition="top center",
        textfont=dict(size=12, color="black", family="Arial Black"),
        marker=dict(color=party_means["color"], size=16, line=dict(color="black", width=1.5)),
        showlegend=False,
        hoverinfo="skip",
    ))

    fig1 = go.Figure(traces)
    fig1.update_layout(
        title="PCA af kandidater — klik på en prik for at se kandidaten",
        xaxis_title=f"PC1 ({var1:.1%}) — Skær ned/udlændinge  ←→  Offentlig transport/bistand/DR",
        yaxis_title=f"PC2 ({var2:.1%}) — Populistisk  ←→  Pragmatisk",
        height=650,
        legend_title="Parti",
        plot_bgcolor="white",
        xaxis=dict(zeroline=True, zerolinecolor="lightgrey", gridcolor="whitesmoke"),
        yaxis=dict(zeroline=True, zerolinecolor="lightgrey", gridcolor="whitesmoke"),
    )

    mo.ui.plotly(fig1)
    return


@app.cell(hide_code=True)
def _(mo, q_text):
    # --- Cell 2: Per-question party bar chart ---
    question_options = {f"Q{i}: {q_text[f'q{i}'][:60]}…": f"q{i}" for i in range(1, 26)}

    question_dropdown = mo.ui.dropdown(
        options=question_options,
        value=list(question_options.keys())[0],
        label="Vælg spørgsmål",
    )
    question_dropdown
    return (question_dropdown,)


@app.cell(hide_code=True)
def _(PARTY_COLORS, df, df_raw, go, mo, question_dropdown):
    selected_q = question_dropdown.value
    q_num = int(selected_q[1:])
    full_question = df_raw[f"q{q_num}_question"].iloc[0]
    label_col = f"q{q_num}_answer_label"
    val_col = f"q{q_num}_answer_value"

    ANSWER_LABELS = {1: "Meget enig", 2: "Enig", 3: "Hverken/eller", 4: "Uenig", 5: "Meget uenig"}

    party_q = df.groupby("party_code")[val_col].mean().sort_values()

    bar_colors = [PARTY_COLORS.get(p, "#888888") for p in party_q.index]

    fig2 = go.Figure(go.Bar(
        x=list(party_q.index),
        y=list(party_q.values),
        marker_color=bar_colors,
        text=[f"{v:.2f}" for v in party_q.values],
        textposition="outside",
    ))
    fig2.update_layout(
        title=f"<b>Gennemsnitligt svar per parti</b><br><sup>{full_question}</sup>",
        xaxis_title="Parti",
        yaxis_title="Gennemsnit (1=Meget enig, 5=Meget uenig)",
        yaxis=dict(range=[1, 5.5], tickvals=[1, 2, 3, 4, 5],
                   ticktext=["1 Meget enig", "2 Enig", "3 Hverken/eller", "4 Uenig", "5 Meget uenig"]),
        height=450,
        plot_bgcolor="white",
        xaxis=dict(gridcolor="whitesmoke"),
    )

    mo.ui.plotly(fig2)
    return


@app.cell(hide_code=True)
def _(mo, q_text):
    # --- Cell 3: PCA colored by a single question's answer ---
    q3_options = {f"Q{i}: {q_text[f'q{i}'][:60]}…": f"q{i}" for i in range(1, 26)}
    q3_dropdown = mo.ui.dropdown(
        options=q3_options,
        value=list(q3_options.keys())[0],
        label="Farvelæg PCA efter spørgsmål",
    )
    q3_dropdown
    return q3_dropdown, q3_options


@app.cell(hide_code=True)
def _(df, df_raw, go, mo, q3_dropdown, var1, var2):
    sel = q3_dropdown.value
    q3_num = int(sel[1:])
    q3_full = df_raw[f"q{q3_num}_question"].iloc[0]
    val_col3 = f"q{q3_num}_answer_value"

    fig3 = go.Figure(go.Scatter(
        x=df["pc1"],
        y=df["pc2"],
        mode="markers",
        marker=dict(
            color=df[val_col3],
            colorscale=[[0, "#2166ac"], [0.25, "#92c5de"], [0.5, "#f7f7f7"],
                        [0.75, "#f4a582"], [1, "#d6604d"]],
            cmin=1, cmax=5,
            size=6,
            opacity=0.75,
            colorbar=dict(
                title="Svar",
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["1 Meget enig", "2 Enig", "3 Hverken/eller", "4 Uenig", "5 Meget uenig"],
                len=0.6,
            ),
            showscale=True,
        ),
        customdata=df[["name", "party_code", val_col3]].values,
        hovertemplate="<b>%{customdata[0]}</b> (%{customdata[1]})<br>Svar: %{customdata[2]}<extra></extra>",
    ))

    fig3.update_layout(
        title=f"<b>PCA farvelagt efter svar</b><br><sup>{q3_full}</sup>",
        xaxis_title=f"PC1 ({var1:.1%}) — Skær ned/udlændinge  ←→  Offentlig transport/bistand/DR",
        yaxis_title=f"PC2 ({var2:.1%}) — Populistisk  ←→  Pragmatisk",
        height=650,
        plot_bgcolor="white",
        xaxis=dict(zeroline=True, zerolinecolor="lightgrey", gridcolor="whitesmoke"),
        yaxis=dict(zeroline=True, zerolinecolor="lightgrey", gridcolor="whitesmoke"),
    )

    mo.ui.plotly(fig3)
    return


@app.cell(hide_code=True)
def _(mo, q_text):
    # --- Cell 4: dropdown for lines+means PCA ---
    q4_options = {f"Q{i}: {q_text[f'q{i}'][:60]}…": f"q{i}" for i in range(1, 26)}
    q4_dropdown = mo.ui.dropdown(
        options=q4_options,
        value=list(q4_options.keys())[0],
        label="Vælg spørgsmål — PCA med linjer til partimiddelværdi",
    )
    q4_dropdown
    return q4_dropdown, q4_options


@app.cell(hide_code=True)
def _(df, df_raw, go, mo, party_means, q4_dropdown, var1, var2):
    sel4 = q4_dropdown.value
    q4_num = int(sel4[1:])
    q4_full = df_raw[f"q{q4_num}_question"].iloc[0]
    val_col4 = f"q{q4_num}_answer_value"

    COLORSCALE4 = [[0, "#2166ac"], [0.25, "#92c5de"], [0.5, "#f7f7f7"],
                   [0.75, "#f4a582"], [1, "#d6604d"]]

    traces4 = []

    # Lines from each candidate to their party mean
    for party4, group4 in df.groupby("party_code"):
        mean_row4 = party_means[party_means["party_code"] == party4].iloc[0]
        lx, ly = [], []
        for _, r in group4.iterrows():
            lx += [r["pc1"], mean_row4["pc1"], None]
            ly += [r["pc2"], mean_row4["pc2"], None]
        traces4.append(go.Scatter(
            x=lx, y=ly, mode="lines",
            line=dict(color="lightgrey", width=0.5),
            opacity=0.4, showlegend=False, hoverinfo="skip",
        ))

    # Candidate dots colored by answer value
    traces4.append(go.Scatter(
        x=df["pc1"], y=df["pc2"],
        mode="markers",
        marker=dict(
            color=df[val_col4], colorscale=COLORSCALE4,
            cmin=1, cmax=5, size=6, opacity=0.8,
            colorbar=dict(
                title="Svar", tickvals=[1, 2, 3, 4, 5],
                ticktext=["1 Meget enig", "2 Enig", "3 Hverken/eller", "4 Uenig", "5 Meget uenig"],
                len=0.6,
            ),
            showscale=True,
        ),
        customdata=df[["name", "party_code", val_col4]].values,
        hovertemplate="<b>%{customdata[0]}</b> (%{customdata[1]})<br>Svar: %{customdata[2]}<extra></extra>",
        showlegend=False,
    ))

    # Party mean dots + labels colored by mean answer
    pm4 = party_means.merge(
        df.groupby("party_code")[val_col4].mean().reset_index().rename(columns={val_col4: "mean_ans"}),
        on="party_code"
    )
    traces4.append(go.Scatter(
        x=pm4["pc1"], y=pm4["pc2"],
        mode="markers+text",
        text=pm4["party_code"],
        textposition="top center",
        textfont=dict(size=12, color="black", family="Arial Black"),
        marker=dict(
            color=pm4["mean_ans"], colorscale=COLORSCALE4,
            cmin=1, cmax=5, size=18,
            line=dict(color="black", width=1.5), showscale=False,
        ),
        showlegend=False,
        hovertemplate="<b>%{text}</b><br>Gennemsnit: %{marker.color:.2f}<extra></extra>",
    ))

    fig4 = go.Figure(traces4)
    fig4.update_layout(
        title=f"<b>PCA med linjer — farvelagt efter svar</b><br><sup>{q4_full}</sup>",
        xaxis_title=f"PC1 ({var1:.1%}) — Skær ned/udlændinge  ←→  Offentlig transport/bistand/DR",
        yaxis_title=f"PC2 ({var2:.1%}) — Populistisk  ←→  Pragmatisk",
        height=650,
        plot_bgcolor="white",
        xaxis=dict(zeroline=True, zerolinecolor="lightgrey", gridcolor="whitesmoke"),
        yaxis=dict(zeroline=True, zerolinecolor="lightgrey", gridcolor="whitesmoke"),
    )

    mo.ui.plotly(fig4)
    return


@app.cell(hide_code=True)
def _(PARTY_COLORS, df, mo):
    # --- Cell 5: Compare 2 parties across all 25 questions ---
    parties = sorted(df["party_code"].unique().tolist())
    party_a = mo.ui.dropdown(options=parties, value="A", label="Parti A")
    party_b = mo.ui.dropdown(options=parties, value="V", label="Parti B")
    mo.hstack([party_a, party_b])
    return party_a, party_b, parties


@app.cell(hide_code=True)
def _(PARTY_COLORS, df, df_raw, go, mo, party_a, party_b):
    pa = party_a.value
    pb = party_b.value
    q_cols5 = [f"q{i}_answer_value" for i in range(1, 26)]
    q_labels = [df_raw[f"q{i}_question"].iloc[0][:55] + "…" for i in range(1, 26)]

    means_a = df[df["party_code"] == pa][q_cols5].mean()
    means_b = df[df["party_code"] == pb][q_cols5].mean()
    diff = means_a - means_b

    color_a = PARTY_COLORS.get(pa, "#888888")
    color_b = PARTY_COLORS.get(pb, "#888888")

    fig5 = go.Figure()

    fig5.add_trace(go.Bar(
        name=pa, x=q_labels, y=means_a,
        marker_color=color_a, opacity=0.85,
    ))
    fig5.add_trace(go.Bar(
        name=pb, x=q_labels, y=means_b,
        marker_color=color_b, opacity=0.85,
    ))
    fig5.add_trace(go.Scatter(
        name="Forskel (A−B)", x=q_labels, y=diff,
        mode="lines+markers",
        line=dict(color="black", width=1.5, dash="dot"),
        marker=dict(size=6, color=diff, colorscale="RdBu_r", cmin=-2, cmax=2,
                    line=dict(color="black", width=0.5)),
        yaxis="y2",
    ))

    fig5.update_layout(
        title=f"<b>Sammenligning: {pa} vs {pb}</b><br><sup>Gennemsnitligt svar per spørgsmål (1=Meget enig, 5=Meget uenig)</sup>",
        barmode="group",
        height=550,
        plot_bgcolor="white",
        xaxis=dict(tickangle=-35, tickfont=dict(size=9), gridcolor="whitesmoke"),
        yaxis=dict(range=[1, 5.5], tickvals=[1, 2, 3, 4, 5],
                   ticktext=["1 ME", "2 E", "3 H/E", "4 U", "5 MU"],
                   title="Gennemsnit", gridcolor="whitesmoke"),
        yaxis2=dict(range=[-2.5, 2.5], title="Forskel (A−B)",
                    overlaying="y", side="right", showgrid=False,
                    zeroline=True, zerolinecolor="lightgrey"),
        legend=dict(orientation="h", y=1.08),
    )

    mo.ui.plotly(fig5)
    return


if __name__ == "__main__":
    app.run()
