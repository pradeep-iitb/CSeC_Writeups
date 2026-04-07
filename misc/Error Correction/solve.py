import cv2
import numpy as np
import itertools
import sys
import math
import random

IMAGE_PATH = "chall.png"
GRID = 5
SIZE = 450
BLOCK = SIZE // GRID

def load():
    img = cv2.imread(IMAGE_PATH, 0)
    if img is None:
        sys.exit(1)
    return img


def split(img):
    arr = []
    for y in range(GRID):
        for x in range(GRID):
            arr.append(img[y*BLOCK:(y+1)*BLOCK, x*BLOCK:(x+1)*BLOCK])
    return arr

def edges(b):
    return b[0,:], b[-1,:], b[:,0], b[:,-1]

def score(a, b):
    return np.sum(a == b)


def compare(a, b):
    at, ab, al, ar = edges(a)
    bt, bb, bl, br = edges(b)
    return {
        "r": score(ar, bl),
        "l": score(al, br),
        "d": score(ab, bt),
        "u": score(at, bb)
    }

def finder(b):
    _, t = cv2.threshold(b, 128, 255, cv2.THRESH_BINARY)
    return np.sum(t == 0) / t.size

def find_finders(blocks):
    vals = []
    for i in range(len(blocks)):
        vals.append((i, finder(blocks[i])))
    vals.sort(key=lambda x: -x[1])
    return [v[0] for v in vals[:3]]

def build(blocks):
    adj = {}
    for i in range(len(blocks)):
        adj[i] = {}
        for j in range(len(blocks)):
            if i == j:
                continue
            adj[i][j] = compare(blocks[i], blocks[j])
    return adj

def best_right(adj, i, used):
    best = None
    best_score = -1
    for j in adj[i]:
        if j in used:
            continue
        s = adj[i][j]["r"]
        if s > best_score:
            best_score = s
            best = j
    return best

def best_down(adj, i, used):
    best = None
    best_score = -1
    for j in adj[i]:
        if j in used:
            continue
        s = adj[i][j]["d"]
        if s > best_score:
            best_score = s
            best = j
    return best

def build_row(start, adj, used):
    row = [start]
    used.add(start)
    cur = start
    for _ in range(GRID-1):
        nxt = best_right(adj, cur, used)
        if nxt is None:
            break
        row.append(nxt)
        used.add(nxt)
        cur = nxt
    return row

def build_grid(blocks, adj, start):
    used = set()
    grid = []
    first = build_row(start, adj, used)
    grid.append(first)
    for y in range(1, GRID):
        new_row = []
        for x in range(GRID):
            above = grid[y-1][x]
            nxt = best_down(adj, above, used)
            if nxt is None:
                for i in range(len(blocks)):
                    if i not in used:
                        nxt = i
                        break
            new_row.append(nxt)
            used.add(nxt)
        grid.append(new_row)
    return grid

def assemble(blocks, grid):
    img = np.zeros((SIZE, SIZE), dtype=np.uint8)
    for y in range(GRID):
        for x in range(GRID):
            img[y*BLOCK:(y+1)*BLOCK, x*BLOCK:(x+1)*BLOCK] = blocks[grid[y][x]]
    return img

def decode(img):
    det = cv2.QRCodeDetector()
    data, _, _ = det.detectAndDecode(img)
    return data

def try_all(blocks, adj, candidates):
    best_img = None
    best_data = ""
    for c in candidates:
        grid = build_grid(blocks, adj, c)
        img = assemble(blocks, grid)
        data = decode(img)
        if data:
            return img, data
        if best_img is None:
            best_img = img
    return best_img, best_data

def rotate_block(b, k):
    return np.rot90(b, k)

def expand_rotations(blocks):
    all_sets = []
    for combo in itertools.product(range(4), repeat=len(blocks)):
        new = []
        for i in range(len(blocks)):
            new.append(rotate_block(blocks[i], combo[i]))
        all_sets.append(new)
        if len(all_sets) > 30:
            break
    return all_sets

def fallback(blocks):
    best = None
    best_score = -1
    for _ in range(100):
        random.shuffle(blocks)
        img = assemble(blocks, [list(range(i*GRID,(i+1)*GRID)) for i in range(GRID)])
        d = decode(img)
        if d:
            return img, d
        s = np.sum(img)
        if s > best_score:
            best_score = s
            best = img
    return best, ""

def main():
    img = load()
    blocks = split(img)
    adj = build(blocks)
    finders = find_finders(blocks)
    img1, data1 = try_all(blocks, adj, finders)
    if data1:
        cv2.imwrite("solved.png", img1)
        print(data1)
        return
    rotations = expand_rotations(blocks)
    for rb in rotations:
        adj2 = build(rb)
        f2 = find_finders(rb)
        img2, data2 = try_all(rb, adj2, f2)
        if data2:
            cv2.imwrite("solved.png", img2)
            print(data2)
            return
    img3, data3 = fallback(blocks)
    cv2.imwrite("solved.png", img3)
    print(data3)

# This is not the script i used it to solve this problem , i tried some questions on Virtual Machine and had the files there , But my Kali Linux got corrupted or something so i had to delete the VM and install again I copied the writeups but forgot the scripts , Last day of submission I tried to generate all deleted files again but this doesnt work for this script .

if __name__ == "__main__":
    main()
