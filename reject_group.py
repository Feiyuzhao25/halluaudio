import matplotlib
matplotlib.use("TkAgg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.transforms as transforms

rcParams['font.family'] = 'DejaVu Sans'
rcParams['font.weight'] = 'bold'
rcParams['text.color'] = '#444444'
rcParams['axes.labelcolor'] = '#444444'
rcParams['xtick.color'] = '#444444'
rcParams['ytick.color'] = '#444444'

BASE_FONT = 14

rcParams['font.size'] = BASE_FONT + 5
rcParams['axes.titlesize'] = BASE_FONT + 5
rcParams['axes.labelsize'] = BASE_FONT + 4
rcParams['xtick.labelsize'] = BASE_FONT + 10
rcParams['ytick.labelsize'] = BASE_FONT + 10
rcParams['legend.fontsize'] = BASE_FONT + 2


csv_path = "D:/results/fsd50/analysis_out/yesno_metrics.csv"
df = pd.read_csv(csv_path)


pastel_colors = [
    "#B5E5FF", "#FFC9A9", "#A7D8F0", "#FFB5C2", "#F7D8BA",
    "#FFCE9E", "#FFE8A3", "#E8DFF5", "#E1C6FF", "#A6EDC5",
    "#FFD1DC", "#C7B8EA", "#B8E9D0", "#FFF3A1", "#9DE3E8",
]
line_styles = ["solid", "dashed", "dashdot", "dotted", (0, (3, 5, 1, 5))]

FILL_THRESHOLD = 1.00


models = df.columns[2:]  # Qwen1, Qwen2, Llama1, ...

def plot_radar(metric_name):
    df_metric = df[df['metric'] == metric_name].reset_index(drop=True)
    labels = df_metric['task'].tolist()
    num_tasks = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_tasks, endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, polar=True)
    ax.set_xticks([])
    ax.xaxis.set_ticklabels([])

    for idx, model in enumerate(models):
        values = df_metric[model].astype(float).tolist()
        values += values[:1]

        num_full = sum(v == 100 for v in df_metric[model].astype(float))

        color = pastel_colors[idx % len(pastel_colors)]
        linestyle = line_styles[idx % len(line_styles)]

        ax.plot(
            angles, values,
            color=color,
            linewidth=2.6 if num_full/num_tasks >= FILL_THRESHOLD else 2.0,
            linestyle=linestyle,
            label=model,
            zorder=10
        )

        if num_full / num_tasks < FILL_THRESHOLD:
            ax.fill(angles, values, color=color, alpha=0.6, zorder=30)

        task_max_values = df_metric[models].astype(float).max(axis=1).tolist()
        r_max = ax.get_ylim()[1]
        label_offset = 0.05 * r_max

        for ang, val in zip(angles[:-1], task_max_values):
            xy = (ang, val)

            offset = transforms.ScaledTranslation(0, 12 / 72, ax.figure.dpi_scale_trans)

            text_transform = ax.transData + offset

            ax.text(
                ang,
                val,
                f"{val:.2f}",
                transform=text_transform,
                fontsize=BASE_FONT-1,
                fontweight="bold",
                color="#333",
                ha="center",
                va="bottom",
                zorder=30,
                bbox=dict(
                    boxstyle="round,pad=0.25",
                    facecolor="white",
                    edgecolor="#555",
                    linewidth=0.8,
                    alpha=0.85,
                )
            )

    r_max = ax.get_ylim()[1]
    label_radius = 1.17 * r_max
    for angle, label in zip(angles[:-1], labels):
        ax.text(
            angle,
            label_radius,
            label,
            fontsize= BASE_FONT + 4,
            fontweight="bold",
            ha="center",
            va="center",
            rotation=0,
            zorder=10,
        )

    ax.grid(color="gray", alpha=0.30, linewidth=2)
    ax.spines["polar"].set_color("black")
    ax.spines["polar"].set_linewidth(2.0)
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", ""],
               fontsize=10, color="#555", fontweight="bold")
    plt.ylim(0, 100)

    plt.title(metric_name, fontsize=22, fontweight="bold", pad=65, color="black")
    plt.legend(loc='upper right', bbox_to_anchor=(1.32, 1.05),
               fontsize=12, frameon=False)
    plt.subplots_adjust(top=0.82)
    plt.tight_layout()
    plt.savefig(
        f"D:/results/fsd50/analysis_out/audio_{metric_name}.svg",
        format="svg",
        dpi=300,
        bbox_inches="tight",
        transparent=True
    )
    plt.show()

metrics = df['metric'].unique()
for m in metrics:
    plot_radar(m)
