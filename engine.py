from PIL import Image, ImageDraw, ImageFont, ImageFilter
import fitz
import os


class WatermarkEngine:

    def apply_text_tile(self, img, text, opacity=80, scale=1, angle=30, emboss=True):
        img = img.convert("RGBA")

        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)

        # FONT
        try:
            font = ImageFont.truetype("arial.ttf", int(40 * scale))
        except:
            font = ImageFont.load_default()

        # TEXT SIZE
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # ======================
        # EMBOSS TEXT
        # ======================
        text_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(text_img)

        if emboss:
            # shadow (gelap)
            d.text((2, 2), text, font=font, fill=(0, 0, 0, int(opacity * 0.6)))

            # highlight (terang)
            d.text((-1, -1), text, font=font, fill=(255, 255, 255, int(opacity * 0.6)))

        # main text
        d.text((0, 0), text, fill=(255, 255, 255, opacity), font=font)

        # blur tipis biar halus
        if emboss:
            text_img = text_img.filter(ImageFilter.GaussianBlur(0.5))

        # ROTATE
        text_img = text_img.rotate(angle, expand=True)

        # ======================
        # TILE (lebih rapat)
        # ======================
        step_x = int(text_img.width * 1.3)
        step_y = int(text_img.height * 1.3)

        for x in range(-img.width, img.width * 2, step_x):
            for y in range(-img.height, img.height * 2, step_y):
                layer.paste(text_img, (x, y), text_img)

        return Image.alpha_composite(img, layer)

    # ======================
    # PREVIEW
    # ======================
    def generate_preview(self, path, text, opacity, scale, emboss):
        if path.lower().endswith(".pdf"):
            doc = fitz.open(path)
            pix = doc[0].get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            doc.close()
        else:
            img = Image.open(path)

        return self.apply_text_tile(img, text, opacity, scale, emboss=emboss)

    # ======================
    # EXPORT
    # ======================
    def process_file(self, input_path, output_path, text, opacity, scale, emboss):
        ext = os.path.splitext(input_path)[1].lower()

        if ext in [".png", ".jpg", ".jpeg"]:
            img = Image.open(input_path)
            result = self.apply_text_tile(img, text, opacity, scale, emboss=emboss)

            if ext in [".jpg", ".jpeg"]:
                result = result.convert("RGB")

            result.save(output_path)

        elif ext == ".pdf":
            doc = fitz.open(input_path)

            for i in range(len(doc)):
                page = doc[i]
                pix = page.get_pixmap()

                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                wm = self.apply_text_tile(img, text, opacity, scale, emboss=emboss)

                temp = f"temp_{i}.png"
                wm.save(temp)

                page.insert_image(page.rect, filename=temp)
                os.remove(temp)

            doc.save(output_path)
            doc.close()