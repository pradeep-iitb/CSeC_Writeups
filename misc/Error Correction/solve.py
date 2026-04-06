from PIL import Image
import numpy as np
from scipy.optimize import linear_sum_assignment

img = Image.open('chall.png')

# Resize to 45x45 (one pixel per module)
qr_45 = img.resize((45, 45), resample=Image.Resampling.NEAREST)
arr = np.array(qr_45)
# Binary: 0=black, 1=white
binary = (arr > 128).astype(np.uint8)

print("45x45 QR modules:")
print(binary)

# Extract 25 chunks of 9x9 modules each
chunks = []
for cy in range(5):
    for cx in range(5):
        chunk = binary[cy*9:(cy+1)*9, cx*9:(cx+1)*9]
        chunks.append((cx, cy, chunk))

# Now score each chunk for each position
# Using QR version 7 known patterns

# Version 7, 45x45
# Finder patterns at:
#   TL: rows 0-6, cols 0-6
#   TR: rows 0-6, cols 38-44
#   BL: rows 38-44, cols 0-6

FINDER = np.array([
    [0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0],
])

# Separator rows/cols (all white=1) around finders
# TL: row 7 cols 0-7, col 7 rows 0-7
# TR: row 7 cols 37-44, col 37 rows 0-7
# BL: row 37 cols 0-7, col 7 rows 37-44

# Timing: row 6 cols 8-36, col 6 rows 8-36
# pattern: 0,1,0,1,0,1...

# Alignment centers for version 7:
# (6,22),(6,38),(22,6),(22,22),(22,38),(38,6),(38,22),(38,38)
ALIGN = np.array([
    [0,0,0,0,0],
    [0,1,1,1,0],
    [0,1,0,1,0],
    [0,1,1,1,0],
    [0,0,0,0,0],
])
ALIGN_CENTERS = [(22,22),(22,38),(38,22),(38,38),
                 (6,22),(22,6),(38,6)]
# Note: (6,38) and (38,6) overlap with finder - skip those

def build_known_mask():
    """
    Build 45x45 array of known module values
    -1 = unknown, 0 = black, 1 = white
    """
    mask = np.full((45,45), -1, dtype=int)
    
    # Finder TL
    mask[0:7, 0:7] = FINDER
    # Finder TR  
    mask[0:7, 38:45] = FINDER
    # Finder BL
    mask[38:45, 0:7] = FINDER
    
    # Separators (white=1)
    mask[7, 0:8] = 1   # TL bottom sep
    mask[0:8, 7] = 1   # TL right sep
    mask[7, 37:45] = 1 # TR bottom sep
    mask[0:8, 37] = 1  # TR left sep
    mask[37, 0:8] = 1  # BL top sep
    mask[38:45, 7] = 1 # BL right sep
    
    # Timing row 6
    for c in range(8, 37):
        mask[6, c] = c % 2  # 0,1,0,1...
    # Timing col 6
    for r in range(8, 37):
        mask[r, 6] = r % 2
    
    # Alignment patterns
    for (ac_r, ac_c) in ALIGN_CENTERS:
        # Check not overlapping finder
        if ac_r < 9 and ac_c < 9: continue
        if ac_r < 9 and ac_c > 35: continue
        if ac_r > 35 and ac_c < 9: continue
        mask[ac_r-2:ac_r+3, ac_c-2:ac_c+3] = ALIGN
    
    # Dark module
    mask[8, 4*7+9] = 0  # version 7: pos (8, 37)
    
    return mask

known = build_known_mask()
print(f"\nKnown modules: {(known >= 0).sum()} / 2025")

def score_chunk_position(chunk_9x9, pos_r, pos_c):
    """
    Score chunk at position (pos_r, pos_c) in 5x5 grid
    pos_r, pos_c in 0..4
    Covers modules [pos_r*9:(pos_r+1)*9, pos_c*9:(pos_c+1)*9]
    """
    r_start = pos_r * 9
    c_start = pos_c * 9
    
    score = 0
    known_count = 0
    
    for r in range(9):
        for c in range(9):
            abs_r = r_start + r
            abs_c = c_start + c
            expected = known[abs_r, abs_c]
            if expected >= 0:
                known_count += 1
                actual = chunk_9x9[r, c]
                if actual == expected:
                    score += 1
                else:
                    score -= 1
    
    return score, known_count

# Extract chunks from scrambled image
chunk_list = []
for cy in range(5):
    for cx in range(5):
        chunk = binary[cy*9:(cy+1)*9, cx*9:(cx+1)*9]
        chunk_list.append(chunk)

print(f"\nTotal chunks: {len(chunk_list)}")

# Score matrix
score_mat = np.zeros((25, 25))
known_mat = np.zeros((25, 25))

for ci, chunk in enumerate(chunk_list):
    for pos in range(25):
        pr, pc = pos // 5, pos % 5
        s, k = score_chunk_position(chunk, pr, pc)
        score_mat[ci, pos] = s
        known_mat[ci, pos] = k

print("\nKnown modules per position:")
print(known_mat[0].reshape(5,5).astype(int))

# Hungarian algorithm
row_ind, col_ind = linear_sum_assignment(-score_mat)

print("\nAssignment (chunk -> position):")
for ci, pos in zip(row_ind, col_ind):
    pr, pc = pos // 5, pos % 5
    s = score_mat[ci, pos]
    k = known_mat[ci, pos]
    print(f"  Chunk({ci//5},{ci%5}) -> Pos({pr},{pc})  score={s:.0f}/{k:.0f}")

# Reconstruct 45x45
recon = np.zeros((45,45), dtype=np.uint8)
for ci, pos in zip(row_ind, col_ind):
    pr, pc = pos // 5, pos % 5
    recon[pr*9:(pr+1)*9, pc*9:(pc+1)*9] = chunk_list[ci]

# Convert to image (upscale for visibility)
recon_img = Image.fromarray((recon * 255).astype(np.uint8))
recon_big = recon_img.resize((450,450), resample=Image.Resampling.NEAREST)
recon_big.save('recon.png')
print("\nSaved recon.png!")

# Print reconstructed QR as text
print("\nReconstructed QR:")
for r in range(45):
    row = ''
    for c in range(45):
        row += '#' if recon[r,c]==0 else ' '
    print(row)

# Verify known modules match
matches = 0
total_known = 0
for r in range(45):
    for c in range(45):
        if known[r,c] >= 0:
            total_known += 1
            if recon[r,c] == known[r,c]:
                matches += 1

print(f"\nKnown module match: {matches}/{total_known} = {100*matches/total_known:.1f}%")
print("If >90% match -> likely correct reconstruction!")