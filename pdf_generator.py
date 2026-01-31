"""
PDF Generator Tool
------------------
Generates professional PDFs from a CSV file with headers, horizontal lines, and footers.

Author: Róbert Zubal
"""

import argparse
import pandas as pd
from fpdf import FPDF
import sys
import os


class PDFGenerator:
    """
    Generates PDFs from a CSV file.

    Attributes:
        csv_path (str): Path to CSV file
        output_path (str): PDF file name
        line_spacing (int): Space between horizontal lines in mm
        font_size (int): Header font size
    """

    def __init__(self, csv_path, output_path="output.pdf", line_spacing=10, font_size=24):
        self.csv_path = csv_path
        self.output_path = output_path
        self.line_spacing = line_spacing
        self.font_size = font_size
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=False, margin=0)

    def generate(self):
        """Reads the CSV and generates the PDF."""
        if not os.path.isfile(self.csv_path):
            print(f"Error: CSV file not found: {self.csv_path}")
            sys.exit(1)

        try:
            df = pd.read_csv(self.csv_path)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            sys.exit(1)

        required_columns = {"Topic", "Pages"}
        if not required_columns.issubset(df.columns):
            print(f"Error: CSV must contain columns: {required_columns}")
            sys.exit(1)

        for _, row in df.iterrows():
            topic = str(row["Topic"])
            pages = int(row.get("Pages", 1))
            self.add_page(topic)  # First page
            for _ in range(pages - 1):
                self.add_page(topic)  # Additional pages

        self.pdf.output(self.output_path)
        print(f"PDF generated successfully: {self.output_path}")

    def add_page(self, topic):
        """Adds a single page with header, horizontal lines, and footer."""
        self.pdf.add_page()

        # Header
        self.pdf.set_font("Arial", "B", size=self.font_size)
        self.pdf.set_text_color(100, 100, 100)
        self.pdf.cell(w=0, h=12, txt=topic, align="L", ln=1)

        # Horizontal lines
        for y in range(20, 298, self.line_spacing):
            self.pdf.line(10, y, 200, y)

        # Footer
        self.pdf.ln(265)
        self.pdf.set_font("Arial", "I", size=8)
        self.pdf.set_text_color(180, 180, 180)
        self.pdf.cell(w=0, h=10, txt=topic, align="R")


def main():
    parser = argparse.ArgumentParser(description="Generate PDFs from CSV topics")
    parser.add_argument("--csv", required=True, help="Path to the CSV file")
    parser.add_argument("--output", default="output.pdf", help="Output PDF file name")
    parser.add_argument("--lines", type=int, default=10, help="Line spacing in mm")
    parser.add_argument("--fontsize", type=int, default=24, help="Header font size")
    args = parser.parse_args()

    generator = PDFGenerator(
        csv_path=args.csv,
        output_path=args.output,
        line_spacing=args.lines,
        font_size=args.fontsize
    )
    generator.generate()


if __name__ == "__main__":
    main()
