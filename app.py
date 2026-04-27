import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import fitz
import os
import io

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class WatermarkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 🔥 WINDOW LEBAR
        self.title("Watermark Tool")
        self.geometry("1200x800")

        self.base_image = None
        self.preview_image = None
        self.tk_image = None

        self.setup_ui()

    # ======================
    # UI
    # ======================
    def setup_ui(self):

        # ===== TOP BAR =====
        top = ctk.CTkFrame(self)
        top.pack(fill="x", pady=10)

        ctk.CTkButton(top, text="Select File", command=self.load_file).pack(side="left", padx=10)
        ctk.CTkButton(top, text="Save", command=self.save_file).pack(side="right", padx=10)

        # ===== PREVIEW =====
        self.preview_label = ctk.CTkLabel(self, text="No file selected")
        self.preview_label.pack(expand=True, fill="both", padx=20, pady=10)

        # ===== CONTROL PANEL =====
        panel = ctk.CTkFrame(self)
        panel.pack(fill="x", padx=20, pady=10)

        # GRID BIAR RAPI
        panel.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # TEXT
        self.text_entry = ctk.CTkEntry(panel, placeholder_text="Watermark Text")
        self.text_entry.insert(0, "SAMPLE")
        self.text_entry.grid(row=0, column=0, columnspan=4, sticky="ew", pady=5)
        self.text_entry.bind("<KeyRelease>", lambda e: self.update_preview())

        # SIZE
        ctk.CTkLabel(panel, text="Size").grid(row=1, column=0)
        self.size_slider = ctk.CTkSlider(panel, from_=10, to=150, command=lambda x: self.update_preview())
        self.size_slider.set(40)
        self.size_slider.grid(row=2, column=0, sticky="ew")

        # OPACITY %
        ctk.CTkLabel(panel, text="Opacity (%)").grid(row=1, column=1)
        self.opacity_slider = ctk.CTkSlider(panel, from_=0, to=100, command=lambda x: self.update_preview())
        self.opacity_slider.set(50)
        self.opacity_slider.grid(row=2, column=1, sticky="ew")

        # COLOR
        ctk.CTkLabel(panel, text="Color (White → Black)").grid(row=1, column=2)
        self.color_slider = ctk.CTkSlider(panel, from_=0, to=255, command=lambda x: self.update_preview())
        self.color_slider.set(255)
        self.color_slider.grid(row=2, column=2, sticky="ew")

        # WATERMARK ROTATION
        ctk.CTkLabel(panel, text="Watermark Rotation").grid(row=1, column=3)
        self.rotation_slider = ctk.CTkSlider(panel, from_=0, to=90, command=lambda x: self.update_preview())
        self.rotation_slider.set(30)
        self.rotation_slider.grid(row=2, column=3, sticky="ew")

        # 🔥 IMAGE ROTATION FIXED
        ctk.CTkLabel(panel, text="Image Rotation").grid(row=3, column=0)
        self.img_rotation_option = ctk.CTkOptionMenu(
            panel,
            values=["0", "90", "180", "270"],
            command=lambda x: self.update_preview()
        )
        self.img_rotation_option.set("0")
        self.img_rotation_option.grid(row=4, column=0, sticky="ew")

        # TILE SPACING
        ctk.CTkLabel(panel, text="Tile Spacing").grid(row=3, column=1)
        self.spacing_slider = ctk.CTkSlider(panel, from_=50, to=300, command=lambda x: self.update_preview())
        self.spacing_slider.set(120)
        self.spacing_slider.grid(row=4, column=1, sticky="ew")

        # EMBOSS
        self.emboss_var = ctk.BooleanVar()
        ctk.CTkSwitch(panel, text="Emboss", variable=self.emboss_var,
                      command=self.update_preview).grid(row=4, column=2)

    # ======================
    # LOAD FILE
    # ======================
    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images/PDF", "*.png *.jpg *.jpeg *.pdf")]
        )
        if not path:
            return

        if path.lower().endswith(".pdf"):
            doc = fitz.open(path)
            page = doc[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_data = pix.tobytes("png")
            self.base_image = Image.open(io.BytesIO(img_data)).convert("RGBA")
            doc.close()
        else:
            self.base_image = Image.open(path).convert("RGBA")

        self.update_preview()

    # ======================
    # WATERMARK
    # ======================
    def apply_watermark(self, image):
        text = self.text_entry.get()
        size = int(self.size_slider.get())

        # OPACITY %
        opacity = int((self.opacity_slider.get() / 100) * 255)

        # COLOR
        gray = int(self.color_slider.get())
        color = (gray, gray, gray, opacity)

        angle = int(self.rotation_slider.get())
        spacing = int(self.spacing_slider.get())

        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        try:
            font = ImageFont.truetype("arial.ttf", size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        text_img = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(text_img)

        if self.emboss_var.get():
            tdraw.text((2, 2), text, font=font, fill=(0, 0, 0, opacity))
            tdraw.text((0, 0), text, font=font, fill=color)
            text_img = text_img.filter(ImageFilter.EMBOSS)
        else:
            tdraw.text((0, 0), text, font=font, fill=color)

        text_img = text_img.rotate(angle, expand=True)

        for x in range(-image.size[0], image.size[0]*2, spacing):
            for y in range(-image.size[1], image.size[1]*2, spacing):
                overlay.paste(text_img, (x, y), text_img)

        return Image.alpha_composite(image, overlay)

    # ======================
    # PREVIEW
    # ======================
    def update_preview(self):
        if not self.base_image:
            return

        img = self.base_image.copy()

        # 🔥 FIXED ROTATION
        rot = int(self.img_rotation_option.get())
        if rot != 0:
            img = img.rotate(rot, expand=True)

        img = self.apply_watermark(img)

        img.thumbnail((1000, 500))
        self.preview_image = img

        self.tk_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        self.preview_label.configure(image=self.tk_image, text="")

    # ======================
    # SAVE
    # ======================
    def save_file(self):
        if not self.base_image:
            return

        output = filedialog.asksaveasfilename(defaultextension=".png")
        if not output:
            return

        img = self.base_image.copy()

        rot = int(self.img_rotation_option.get())
        if rot != 0:
            img = img.rotate(rot, expand=True)

        result = self.apply_watermark(img)
        result.save(output)

        print("Saved:", output)


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()