from pathlib import Path

from pathlib import Path

font_path = Path(__file__).parent / "DejaVuSans.ttf"  # Searches in the script's directory

if not font_path.exists():
    raise FileNotFoundError(f"{font_path} font file not found! Please add it to the project folder.")

# Load the font into FPDF
self.add_font("DejaVu", style="", fname=str(font_path), uni=True)
