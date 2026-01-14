import os
import sys
import pikepdf
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def load_pdf(path):
    """Try opening PDF with pikepdf. Return (path, pdf or None)."""
    try:
        return path, pikepdf.open(path)
    except Exception as e:
        print(f"⚠️ Skipping {os.path.basename(path)} (error: {e})")
        return path, None

def merge_pdfs(output_filename):
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Collect PDFs sorted by (length, then alphabetically)
    pdf_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".pdf")
    ]
    pdf_files.sort(key=lambda x: (len(os.path.basename(x)), os.path.basename(x).lower()))

    if not pdf_files:
        print("❌ No PDF files found in input folder.")
        return

    # Auto CPU-based threading
    max_threads = min(32, (os.cpu_count() or 1) + 4)
    print(f"⚡ Using {max_threads} threads for parallel PDF loading")

    results = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(load_pdf, pdf) for pdf in pdf_files]
        for future in tqdm(as_completed(futures), total=len(pdf_files), desc="Loading PDFs"):
            path, pdf = future.result()
            if pdf is not None:
                results.append((path, pdf))

    # Preserve correct order
    results.sort(key=lambda x: (len(os.path.basename(x[0])), os.path.basename(x[0]).lower()))

    # Merge using pikepdf
    merged = pikepdf.Pdf.new()
    for path, pdf in tqdm(results, desc="Merging PDFs", unit="file"):
        merged.pages.extend(pdf.pages)

    # Ensure .pdf extension
    if not output_filename.lower().endswith(".pdf"):
        output_filename += ".pdf"

    output_path = os.path.join(output_dir, output_filename)
    merged.save(output_path)

    print(f"\n✅ Merged PDF saved as: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fast_pdf_merger.py <output_filename.pdf>")
    else:
        merge_pdfs(sys.argv[1])
