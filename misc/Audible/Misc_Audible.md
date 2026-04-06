# Misc Challenge — Audible

## How I Started

I began by searching Google for different ways to hide data inside an audio file. Since the challenge was clearly about audio steganography, I first wanted to understand the common hiding techniques before jumping into tools.

I checked a mix of sources:
- Google results about audio steganography methods
- YouTube videos explaining hidden-data techniques
- a random CTF writeup about ways to hide data in media files

That gave me a few obvious directions to test.

## Early Attempts That Did Not Work

My first instinct was to try **LSB-style hiding**, the same idea often used for images, and inspect the audio in a hex editor. I also tried a few Linux tools that are commonly used for audio inspection and extraction.

Those attempts did not give me anything useful. The hidden payload was not exposed that way, so I moved on instead of brute-forcing the wrong direction.

## Sonic Visualiser Discovery

I then came across **Sonic Visualiser** through an AI message and searched YouTube to learn how to use it properly. That turned out to be the right direction.

The important clue was that the hidden data was not really meant to be heard directly. It was embedded visually inside the waveform/spectrogram representation.

## Final Decode

Inside Sonic Visualiser, I adjusted the display settings until the hidden pattern became readable. The key steps were:

1. Load the audio into Sonic Visualiser.
2. Open the spectrogram / graph view instead of relying on normal playback.
3. Change the scaling so the hidden signal became visible.
4. Tweak the color settings until the contrast made the embedded text stand out.

Once the graph was scaled correctly and the colors were tuned, the hidden content became readable and I could extract the flag.

## Result

The challenge was solved by visualization rather than direct audio playback or hex-level extraction.

## Flag

CSeC{Maam_Am_I_Audible}
