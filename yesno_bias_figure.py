import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.rcParams.update({
    "font.size": 17,
    "axes.titlesize": 20,
    "axes.labelsize": 17,
    "xtick.labelsize": 15,
    "ytick.labelsize": 17,
})

file_paths = [
    ("D:results/audiohallu/analysis_out/reject_metrics.csv", "speech_refusal_rate"),
    ("D:results/fsd50/analysis_out/reject_metrics.csv", "audio_refusal_rate"),
    ("D:results/music/analysis_out/reject_metrics.csv", "music_refusal_rate"),
]

color_maps = ["Reds", "Blues", "Greens"]

for (csv_path, name), cmap in zip(file_paths, color_maps):
    save_dir = os.path.dirname(csv_path)
    os.makedirs(save_dir, exist_ok=True)

    df = pd.read_csv(csv_path, encoding="utf-8")
    df_plot = df.set_index("task")

    plt.figure(figsize=(12.5, 8))

    ax = sns.heatmap(
        df_plot,
        annot=True,
        fmt=".1f",
        cmap=cmap,
        annot_kws={"size": 20},  # 🔥 热力图数字
        linewidths=0.5
    )

    # ax.set_title(name.replace("_", " ").title(), fontsize=22, fontweight="bold", pad=65, color="black")
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")

    ax.tick_params(axis="x", labelsize=16)
    ax.tick_params(axis="y", labelsize=16)

    plt.tight_layout()

    save_path = os.path.join(save_dir, f"{name}.svg")
    plt.savefig(save_path, format="svg")
    plt.close()
