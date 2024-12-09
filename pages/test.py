from pathlib import Path

font_path = Path("/Users/dr.ajayshukla/PycharmProjects/Panini_nutrition/DejaVuSans.ttf")

if font_path.exists():
    print("Font exists and is accessible!")
else:
    print("Font not found or inaccessible.")
