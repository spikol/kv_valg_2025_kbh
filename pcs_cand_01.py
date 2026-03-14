import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

df_raw = pd.read_csv("folk_version_03/combined_wide.csv")

cols = ["candidate_id", "name", "party_code"] + [f"q{i}_answer_value" for i in range(1, 26)]
df = df_raw[cols].dropna().copy()

q_cols = [f"q{i}_answer_value" for i in range(1, 26)]

# Danish standard party colors
PARTY_COLORS = {
    "A": "#E3001B",  # Socialdemokratiet
    "B": "#733B80",  # Radikale Venstre
    "C": "#006437",  # Konservative
    "F": "#F04E23",  # SF
    "H": "#B5C400",  # Frie Grønne
    "I": "#00AEEF",  # Liberal Alliance
    "M": "#00827F",  # Moderaterne
    "O": "#F5A623",  # Dansk Folkeparti
    "V": "#002883",  # Venstre
    "X": "#888888",  # Other
    "Æ": "#8B1A1A",  # Danmarksdemokraterne
    "Ø": "#C0392B",  # Enhedslisten
    "Å": "#2ECC71",  # Alternativet
}

# 1. Scale on individual candidate data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[q_cols])

# 2. PCA
pca = PCA(n_components=2)
coords = pca.fit_transform(X_scaled)
coords[:, 0] *= -1  # flip PC1 to match orientation

print(f"Variance explained: PC1={pca.explained_variance_ratio_[0]:.1%}, PC2={pca.explained_variance_ratio_[1]:.1%}")

df = df.copy()
df["pc1"] = coords[:, 0]
df["pc2"] = coords[:, 1]

# 3. Plot candidates, colored by party
fig, ax = plt.subplots(figsize=(12, 9))

for party, group in df.groupby("party_code"):
    color = PARTY_COLORS.get(party, "#888888")
    ax.scatter(group["pc1"], group["pc2"], s=15, color=color, alpha=0.5, label=party)

# Overlay party mean labels
party_means = df.groupby("party_code")[["pc1", "pc2"]].mean()
for party, row in party_means.iterrows():
    color = PARTY_COLORS.get(party, "#888888")
    ax.scatter(row["pc1"], row["pc2"], s=120, color=color, edgecolors="black", linewidths=0.8, zorder=5)
    ax.annotate(party, (row["pc1"], row["pc2"]), fontsize=10,
                ha="center", va="bottom", color="black", fontweight="bold")

ax.axhline(0, color="grey", lw=0.5)
ax.axvline(0, color="grey", lw=0.5)
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})  —  venstre/udlændinge/DR", fontsize=11)
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})  —  pensionsalder/Ukraine", fontsize=11)
ax.set_title("PCA af kandidater (DR Kandidatest) — distrikter 6-27 Kbh", fontsize=13)
ax.legend(title="Parti", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)

plt.tight_layout()
plt.savefig("folk_version_03/pca_candidates.png", dpi=150)
plt.show()
