
from pathlib import Path
import fitz  # PyMuPDF
import numpy as np


def crop_pdf_to_visible_content(
    input_pdf,
    output_pdf,
    dpi=300,
    threshold=250,
    padding_pt=0.0,
):
    """
    按渲染后的非白色像素边界裁剪 PDF 页面，让上下左右尽量没有留白。

    参数
    ----
    input_pdf:
        输入 PDF 路径。
    output_pdf:
        输出裁剪后的 PDF 路径。
    dpi:
        用于检测白边的渲染分辨率。越高越精细，但越慢。
    threshold:
        白色阈值。RGB 三个通道都 >= threshold 的像素会被视为白色背景。
        通常 245-252 都可以。数值越高，裁剪越保守。
    padding_pt:
        裁剪后额外保留的边距，单位 pt。若想几乎无留白，用 0。
    """
    input_pdf = Path(input_pdf)
    output_pdf = Path(output_pdf)

    doc = fitz.open(str(input_pdf))
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    for page in doc:
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )

        # 非白色像素 mask
        # alpha=False 时通常是 RGB；保险起见只取前三个通道
        rgb = img[:, :, :3]
        non_white = np.any(rgb < threshold, axis=2)

        if not non_white.any():
            continue

        ys, xs = np.where(non_white)
        x0_px, x1_px = xs.min(), xs.max() + 1
        y0_px, y1_px = ys.min(), ys.max() + 1

        # PyMuPDF 坐标系也是左上为原点，因此像素坐标可以直接换算为 page 坐标
        x0 = page.rect.x0 + x0_px / zoom - padding_pt
        y0 = page.rect.y0 + y0_px / zoom - padding_pt
        x1 = page.rect.x0 + x1_px / zoom + padding_pt
        y1 = page.rect.y0 + y1_px / zoom + padding_pt

        # 防止越界
        crop_rect = fitz.Rect(
            max(page.rect.x0, x0),
            max(page.rect.y0, y0),
            min(page.rect.x1, x1),
            min(page.rect.y1, y1),
        )

        page.set_cropbox(crop_rect)

    doc.save(str(output_pdf), garbage=4, deflate=True)
    doc.close()
    return output_pdf


def render_pdf_first_page(pdf_path, output_png, dpi=180):
    """渲染第一页，用于快速检查裁剪结果。"""
    pdf_path = Path(pdf_path)
    output_png = Path(output_png)

    doc = fitz.open(str(pdf_path))
    page = doc[0]
    zoom = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    pix.save(str(output_png))
    doc.close()
    return output_png


if __name__ == "__main__":
    input_pdf = "/ssd1/lbh/zjx/skyjury/analysis/figures/skyjury_circle_bar_no_whitespace.pdf"
    output_pdf = "/ssd1/lbh/zjx/skyjury/analysis/figures/skyjury_circle_bar_no_whitespace_cropped.pdf"
    preview_png = "/ssd1/lbh/zjx/skyjury/analysis/figures/skyjury_circle_bar_no_whitespace_cropped_preview.png"

    crop_pdf_to_visible_content(
        input_pdf=input_pdf,
        output_pdf=output_pdf,
        dpi=300,
        threshold=250,
        padding_pt=0.0,
    )
    render_pdf_first_page(output_pdf, preview_png)

    print("cropped pdf saved to:", output_pdf)
    print("preview png saved to:", preview_png)
