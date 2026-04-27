# 🖼️ Watermark Tool (Python GUI)

A lightweight desktop application to add **text-based watermarks** to images and PDFs with **real-time preview**.

Built using:

* `customtkinter` (modern GUI)
* `Pillow` (image processing)
* `PyMuPDF` (PDF rendering)

---

## ✨ Features

* 🔍 **Live Preview (real-time)**
* 📝 Custom text watermark
* 🔄 **Fixed image rotation** (0°, 90°, 180°, 270°)
* 🔁 Watermark rotation (angle control)
* 🎚️ Opacity control (0–100%)
* 🎨 Grayscale color (white → black)
* 🧱 Tile watermark (full-page diagonal)
* 🧊 Emboss effect (better visibility on light backgrounds)
* 📄 Supports:

  * Images: PNG, JPG, JPEG
  * PDF (first page preview)

---

## 🖥️ UI Overview

```
![Watermark Tool UI](https://github.com/user-attachments/assets/b301943c-b4f0-454e-8774-9d9ed49ebcc9)
```

---

## 📦 Installation

### 1. Clone repository

```bash
git clone https://github.com/yourusername/watermark-tool.git
cd watermark-tool
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python app.py
```

---

## 🧠 How It Works

1. Load image or PDF
2. Adjust watermark settings:

   * Text
   * Size
   * Opacity
   * Color
   * Rotation
3. Preview updates instantly
4. Save output file

---

## ⚙️ Configuration

### Opacity

* Range: **0–100%**
* Internally converted to RGBA (0–255)

### Color (Grayscale)

* `255` → White
* `0` → Black

### Tile Watermark

Watermark is repeated across the canvas:

```python
for x in range(-width, width * 2, spacing):
    for y in range(-height, height * 2, spacing):
```

---

## 📁 Output Formats

* PNG
* JPG

---

## ⚠️ Limitations

* PDF preview only shows the **first page**
* No batch processing (yet)
* No image/logo watermark (text only)
* Font fallback used if `arial.ttf` is not found

---

## 🚀 Roadmap

Planned improvements:

* [ ] Batch watermark (multiple files)
* [ ] Multi-page PDF processing
* [ ] Drag watermark positioning
* [ ] Custom font (TTF selector)
* [ ] Auto contrast watermark (smart visibility)
* [ ] Export directly to PDF

---

## 🧪 Use Cases

* Protect personal documents
* Watermark shared images
* Add branding to files
* Simple document marking

---

## 📜 License

Free for personal and educational use.

---

## 🙌 Author

Developed as a personal research project in:

* Programming
* GUI Development
* Image Processing

---

## 💡 Notes

This tool is designed to be:

* Simple
* Fast
* Lightweight

Alternative heavy tools:

* Adobe Photoshop
* GIMP

---

**Build. Test. Improve. 🚀**
