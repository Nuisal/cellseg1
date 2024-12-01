import copy
import io

import pandas as pd
import streamlit as st
from PIL import Image
from figures.utils.modified_circos import Circos

from figures.utils.figure_1 import add_background_to_polar_fig, create_annular_image
from figures.utils.load_data import load_color, load_figure_1_1_data, load_short_names
from figures.utils.load_image import load_gt_images

st.title("Figure_1_1")


def draw_background_image_tissuenet(images, rotation_angle=0):
    inner_radius = 420
    outer_radius = 730
    num_vertices_per_sector = 200
    gap_angle = 1

    canvas_size = (1500, 1500)
    offsets = [
        (25, 280),
        (0, 0),
        (-50, -100),
        (50, -50),
        (50, -50),
    ]
    scales = [2.5, 0.6, 1.0, 0.8, 2.5]

    background_image = create_annular_image(
        images,
        inner_radius,
        outer_radius,
        canvas_size,
        gap_angle=gap_angle,
        offsets=offsets,
        scales=scales,
        num_vertices_per_sector=num_vertices_per_sector,
        rotation_angle=rotation_angle,
    )
    background_image = Image.fromarray(background_image)
    return background_image


def label_kws_handler(col_name):
    return dict(size=24, font="Arial")


def grid_label_formatter(label):
    return f"{label:.1f}"


def line_kws_handler(col_name):
    return dict(lw=3)


dicts, max_id_dict = load_figure_1_1_data()

df = pd.DataFrame(dicts).T

dataset_order = [
    "DSB",
    "CSB",
    "ECB",
    "BSF",
    "CPS",
]
df = df[dataset_order]

short_name, reversed_short_name = load_short_names()

images = []
for dataset in dataset_order:
    long_name = reversed_short_name[dataset]
    train_id = max_id_dict[long_name]
    image, _, _ = load_gt_images(dataset=long_name, train_or_test="train", select_ids=[train_id])
    images.extend(image)

background_image = draw_background_image_tissuenet(images, rotation_angle=234.9)

method_colors = load_color()

circos = Circos.radar_chart(
    df,
    vmin=0.0,
    vmax=1.0,
    r_lim=(0, 54.6),
    fill=False,
    circular=True,
    marker_size=0,
    bg_color="#FFFFFFFF",
    grid_interval_ratio=0.2,
    cmap=method_colors,
    show_grid_label=True,
    label_kws_handler=label_kws_handler,
    line_kws_handler=line_kws_handler,
    grid_line_kws=dict(lw=1, color="#CCCCCC"),
    grid_label_formatter=grid_label_formatter,
    grid_label_kws=dict(size=22, color="#000000", font="Arial"),
)

fig = circos.plotfig(dpi=300, figsize=(8, 8))

add_background_to_polar_fig(fig, background_image, zoom=0.328)


fig_copy = copy.deepcopy(fig)

st.pyplot(fig, use_container_width=True)

buffer = io.BytesIO()
fig_copy.savefig(buffer, format="pdf")
buffer.seek(0)

if st.download_button(label="Download PDF", data=buffer, file_name="figure_1_1.pdf", mime="application/pdf"):
    pass