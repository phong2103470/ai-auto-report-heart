import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

with open("data/noidung_thuyettrinh.md", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# Slide 1: Slide tiêu đề
title_slide = prs.slides.add_slide(prs.slide_layouts[0])
title_slide.shapes.title.text = lines[0].replace("# ", "")
title_slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(7, 59, 102)
title_slide.shapes.title.text_frame.paragraphs[0].font.bold = True
title_slide.placeholders[1].text = lines[1]

current_slide = None
current_bullets = []
current_image = None

def flush_slide(slide, bullets, image_path):
    if slide is None:
        return
    has_img = image_path and os.path.exists(image_path)
    box_width = Inches(6.2) if has_img else Inches(11.8)
    txBox = slide.shapes.add_textbox(Inches(0.7), Inches(1.6), box_width, Inches(5.2))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(20)
        p.space_after = Pt(14)
    if has_img:
        slide.shapes.add_picture(image_path, Inches(7.1), Inches(1.7), width=Inches(5.6))

for line in lines[2:]:
    if line.startswith("## "):
        flush_slide(current_slide, current_bullets, current_image)
        current_slide = prs.slides.add_slide(prs.slide_layouts[5])
        title_shape = current_slide.shapes.title
        title_shape.text = line.replace("## ", "")
        title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(11, 111, 164)
        title_shape.text_frame.paragraphs[0].font.bold = True
        current_bullets = []
        current_image = None
    elif line.startswith("[IMAGE:") and line.endswith("]"):
        current_image = line.replace("[IMAGE:", "").replace("]", "").strip()
    elif line.startswith("- "):
        current_bullets.append(line[2:])

flush_slide(current_slide, current_bullets, current_image)
prs.save("output/bai_thuyet_trinh_tu_dong.pptx")
print("Hoàn tất Bài cá nhân 2 -> output/bai_thuyet_trinh_tu_dong.pptx")