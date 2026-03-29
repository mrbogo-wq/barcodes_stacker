import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def generate_barcode_pdf(root_dir, output_filename):
    c = canvas.Canvas(output_filename, pagesize=A4)
    width, height = A4
    
    # Configuration based on your image
    img_w, img_h = 90 * mm, 30 * mm  # Approximate barcode size
    v_spacing = 5 * mm               # Gap between stacked barcodes
    margin = 8 * mm                # Page margins
    
    # Define the 4 corner starting positions (bottom-left of each set)
    # Positions are: [Top-Left, Top-Right, Bottom-Left, Bottom-Right]
    corners = [
        (margin, height - margin - (img_h * 3 + v_spacing * 2)),
        (width - margin - img_w, height - margin - (img_h * 3 + v_spacing * 2)),
        (margin, margin),
        (width - margin - img_w, margin)
    ]

    all_barcodes = []
    
    # 1. Collect all paths from branch1, branch2, etc.
    # Sorted to ensure branch1 comes before branch2
    branches = sorted([d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))])
    
    for branch in branches:
        branch_path = os.path.join(root_dir, branch)
        # Sort files by the number in "barcode (X).gif"
        files = [f for f in os.listdir(branch_path) if f.endswith(".gif")]
        files.sort(key=lambda x: int(x.split('(')[1].split(')')[0]))
        
        for f in files:
            all_barcodes.append(os.path.join(branch_path, f))

    # 2. Distribute onto pages
    for i in range(0, len(all_barcodes), 4):
        page_items = all_barcodes[i:i+4]
        
        for idx, img_path in enumerate(page_items):
            base_x, base_y = corners[idx]
            
            # Place 3 of the same barcode stacked vertically
            for row in range(3):
                current_y = base_y + (row * (img_h + v_spacing))
                # preserveAspectRatio ensures no deformation
                c.drawImage(img_path, base_x, current_y, width=img_w, height=img_h, preserveAspectRatio=True)
        
        c.showPage() # Create new page after 4 sets

    c.save()
    print(f"Success! PDF saved as {output_filename}")

# Usage
generate_barcode_pdf("barcodes", "Final_Barcodes_Layout.pdf")
