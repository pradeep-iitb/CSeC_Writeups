# Misc Challenge — Error Correction / QR

## How I Started

This challenge took me the longest. I first had to understand what the generator script was doing before I could even think about solving the QR itself.

My first step was to read the script and figure out how the pieces of the QR were being arranged. Based on that, I wrote a rough script of my own to reorder the chunks and prepare the image for further changes.

## Learning the QR Basics

After that, I spent time learning the basics of QR design and structure. I kept rewriting the script again and again as I understood more about:

- the fixed finder patterns in the corners
- how the remaining modules should line up around them
- how the QR grid behaves when pieces are swapped

## First Scoring-Based Attempt

For one attempt, I generated a script that fixed the three large corner boxes and then randomly swapped the remaining parts. I used the output score from the script as a rough way to judge how close a candidate QR was to being valid. I do not remember the exact name of the metric (I found it in a YT short), but it worked like a fitness score for selecting better layouts.

Using that approach, I generated more than 40 QR candidates and scanned them one by one.

That still did not produce a successful decode.

## Final Breakthrough

At that point, I stopped trying random rearrangements and studied QR codes in detail for about an hour.

I also watched a YouTube lecture on QR internals/error correction, and that helped me understand why my earlier generated candidates were not scannable.

With that deeper understanding, I wrote a much better script. Most of the code came from AI assistance, with only small changes from my side, but it finally handled the QR structure correctly.

The final script was able to place the pieces in the right order, preserve the important alignment around the fixed corner markers, and generate a QR that actually scanned.

## Result

Once the corrected QR was generated, the scanner immediately picked it up and the hidden content was revealed.

## Exploit (Explicit)

The exploit is **reconstruction of a deliberately scrambled QR by respecting QR structural constraints**. The challenge relied on disordering module blocks; solving it required restoring valid QR layout and error-correction consistency.

## How to Prevent This

1. If the goal is stronger resistance, combine scrambling with cryptographic protection of payload, not only visual reordering.
2. Avoid leaving enough deterministic structure that can be reconstructed with guided search.
3. Use integrity checks tied to secret keys rather than decoder tolerance alone.

## Difficulties Faced

1. My initial 50+ generated QR outputs did not scan.
2. I underestimated how strict QR placement and  behavior are.
3. The challenge required understanding QR standards deeply, not only brute-force swaps.

## What I Learned

1. Finder/alignment rules are critical to practical QR recovery.
2. Fitness-style heuristics can help but are insufficient without structural correctness.
3. Targeted external learning (like the QR lecture) can unblock hard reverse-style misc challenges.

## Flag

`CSeC{gO0D_J0b}`
