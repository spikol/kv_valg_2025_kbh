import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

df_raw = pd.read_csv("folk_version_03/combined_wide.csv")

cols = ["candidate_id", "name", "party_code"] + [f"q{i}_answer_value" for i in range(1, 26)]
df = df_raw[cols].copy()
df.to_csv("folk_version_03/pca_input.csv", index=False)

q_cols = [f"q{i}_answer_value" for i in range(1, 26)]

# Candidate count per party
party_counts = df["party_code"].value_counts().sort_index()
print("Kandidater per parti:")
for party, count in party_counts.items():
    print(f"  {party}: {count}")
print(f"  Total: {party_counts.sum()}\n")

# 1. Aggregate by party
party_df = df.groupby("party_code")[q_cols].mean()

# 2. Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(party_df)

# 3. PCA
pca = PCA(n_components=2)
coords = pca.fit_transform(X_scaled)
coords[:, 0] *= -1  # flip PC1 to match v02 orientation

print(f"Variance explained: PC1={pca.explained_variance_ratio_[0]:.1%}, PC2={pca.explained_variance_ratio_[1]:.1%}")

# Question text lookup (from first row of combined_wide.csv)
q_text = {f"q{i}_answer_value": df_raw[f"q{i}_question"].iloc[0] for i in range(1, 26)}

# Print top 5 questions driving each PC
for pc_idx, pc_name in enumerate(["PC1", "PC2"]):
    loadings = pd.Series(pca.components_[pc_idx], index=q_cols)
    top = loadings.abs().nlargest(5).index
    print(f"\n--- {pc_name} top questions ---")
    for q in top:
        print(f"  [{loadings[q]:+.2f}] {q_text[q]}")

# Danish standard party colors
PARTY_COLORS = {
    "A": "#E3001B",  # Socialdemokratiet
    "B": "#733B80",  # Radikale Venstre
    "C": "#006437",  # Konservative
    "F": "#F04E23",  # SF
    "H": "#B5C400",  # Frie Grønne (placeholder)
    "I": "#00AEEF",  # Liberal Alliance
    "M": "#00827F",  # Moderaterne
    "O": "#F5A623",  # Dansk Folkeparti
    "V": "#002883",  # Venstre
    "Æ": "#8B1A1A",  # Danmarksdemokraterne
    "Ø": "#C0392B",  # Enhedslisten
    "Å": "#2ECC71",  # Alternativet
}

# 4. Plot
fig, ax = plt.subplots(figsize=(9, 7))
for i, party in enumerate(party_df.index):
    color = PARTY_COLORS.get(party, "#888888")
    n = party_counts.get(party, 0)
    ax.scatter(coords[i, 0], coords[i, 1], s=200, color=color, zorder=3)
    ax.annotate(f"{party} (n={n})", (coords[i, 0], coords[i, 1]), fontsize=10,
                ha="center", va="bottom", color="black", fontweight="bold")

ax.axhline(0, color="grey", lw=0.5)
ax.axvline(0, color="grey", lw=0.5)

ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})  —  venstre/udlændinge/DR", fontsize=11)
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})  —  pensionsalder/Ukraine", fontsize=11)
ax.set_title("PCA of party positions (mean responses based DR Kandidatest) — 6-27 distrikter Kbh")

# Directional annotations
ax.annotate("← Skær ned / stram udlændingepolitik", xy=(0.02, 0.01), xycoords="axes fraction",
            fontsize=8, color="grey", ha="left")
ax.annotate("Offentlig transport / bistand / DR →", xy=(0.98, 0.01), xycoords="axes fraction",
            fontsize=8, color="grey", ha="right")
ax.annotate("← Populistisk /\nvelferdsøkonomi", xy=(0.01, 0.02), xycoords="axes fraction",
            fontsize=8, color="grey", ha="left", va="bottom", rotation=90)
ax.annotate("Pragmatisk økonomi /\ncenterregering →", xy=(0.01, 0.98), xycoords="axes fraction",
            fontsize=8, color="grey", ha="left", va="top", rotation=90)
plt.tight_layout()
plt.savefig("folk_version_03/pca_parties.png", dpi=150)
plt.show()
