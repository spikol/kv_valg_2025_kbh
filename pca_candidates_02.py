import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

df_raw = pd.read_csv("folk_version_03/combined_wide.csv")

cols = ["candidate_id", "name", "party_code"] + [f"q{i}_answer_value" for i in range(1, 26)]
df = df_raw[cols].dropna().copy()

q_cols = [f"q{i}_answer_value" for i in range(1, 26)]

PARTY_COLORS = {
    "A": "#E3001B",
    "B": "#733B80",
    "C": "#006437",
    "F": "#F04E23",
    "H": "#B5C400",
    "I": "#00AEEF",
    "M": "#00827F",
    "O": "#F5A623",
    "V": "#002883",
    "X": "#888888",
    "Æ": "#8B1A1A",
    "Ø": "#C0392B",
    "Å": "#2ECC71",
}

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[q_cols])

pca = PCA(n_components=2)
coords = pca.fit_transform(X_scaled)
coords[:, 0] *= -1

print(f"Variance explained: PC1={pca.explained_variance_ratio_[0]:.1%}, PC2={pca.explained_variance_ratio_[1]:.1%}")

df = df.copy()
df["pc1"] = coords[:, 0]
df["pc2"] = coords[:, 1]

party_means = df.groupby("party_code")[["pc1", "pc2"]].mean()

fig, ax = plt.subplots(figsize=(14, 10))

for party, group in df.groupby("party_code"):
    color = PARTY_COLORS.get(party, "#888888")
    mx, my = party_means.loc[party, "pc1"], party_means.loc[party, "pc2"]

    # Lines from each candidate to party mean
    for _, row in group.iterrows():
        ax.plot([row["pc1"], mx], [row["pc2"], my],
                color=color, alpha=0.15, lw=0.5, zorder=1)

    # Candidate dots
    ax.scatter(group["pc1"], group["pc2"], s=15, color=color, alpha=0.5, zorder=2, label=party)

# Party mean dots + labels
for party, row in party_means.iterrows():
    color = PARTY_COLORS.get(party, "#888888")
    ax.scatter(row["pc1"], row["pc2"], s=150, color=color,
               edgecolors="black", linewidths=0.9, zorder=5)
    ax.annotate(party, (row["pc1"], row["pc2"]),
                xytext=(0, 8), textcoords="offset points",
                fontsize=10, ha="center", va="bottom", color="black", fontweight="bold")

ax.axhline(0, color="grey", lw=0.5)
ax.axvline(0, color="grey", lw=0.5)
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})  —  venstre/udlændinge/DR", fontsize=11)
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})  —  pensionsalder/Ukraine", fontsize=11)

# Directional annotations
ax.annotate("← Skær ned / stram udlændingepolitik", xy=(0.02, 0.01), xycoords="axes fraction",
            fontsize=8, color="grey", ha="left")
ax.annotate("Offentlig transport / bistand / DR →", xy=(0.98, 0.01), xycoords="axes fraction",
            fontsize=8, color="grey", ha="right")
ax.annotate("← Populistisk /\nvelferdsøkonomi", xy=(0.01, 0.02), xycoords="axes fraction",
            fontsize=8, color="grey", ha="left", va="bottom", rotation=90)
ax.annotate("Pragmatisk økonomi /\ncenterregering →", xy=(0.01, 0.98), xycoords="axes fraction",
            fontsize=8, color="grey", ha="left", va="top", rotation=90)
ax.set_title("PCA af kandidater med linjer til partimiddelværdi (DR Kandidatest) — distrikter 6-27 Kbh", fontsize=12)
ax.legend(title="Parti", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)

plt.tight_layout()
plt.savefig("folk_version_03/pca_candidates_02.png", dpi=150)
plt.show()
