# Don - CTF Writeup

## Challenge Summary
The challenge hint said Don hid the flag in the underworld. The provided files looked unusual at first, but the directory structure (for example `region`, `playerdata`, `poi`, `level.dat`) matched a **Minecraft Java world save**.

## Initial Recon
1. Opened the provided challenge files and identified Minecraft world artifacts.
2. Confirmed this was a world-forensics / in-game investigation challenge, not a normal script or binary execution challenge.
3. Imported the world into the Minecraft saves directory.

## Problems Faced
1. On loading the world, I spawned in lava repeatedly and died in a loop.
2. Because of repeated deaths, direct exploration was not possible.
3. While exploring later, I accidentally broke blocks in the dragon structure, which made me suspect I could have destroyed a clue.

## Recovery Steps
1. Used **NBTExplorer** to modify `level.dat` for spawning coordinates , gamemode , etc , so I could spawn safely and continue exploration.
2. After accidental block destruction, restored the world state by replacing the modified world region with a fresh copy from the original files.

## Key Clue
Inside/near the dragon area, a hanging sign provided the intended hint:

> **Chall 2:**  
> **Emreald**  
> **Blocks are**  
> **Beautiful**

(Maybe spelling in-game is intentionally `Emreald`.)

## Final Discovery
Following the emerald-block clue, I searched beneath/around that clue area and found the flag in a chest.

## Note on Intended vs Unintended Path
After submitting the flag, I discussed my approach with the manager. They confirmed my way of solving was not the intended one . Then I serached in the region file for the message "Emereald Blocks are beautiful" and under it the chest data with custom message VishwasCTF{m1n3cr4f7_15_fun}

While validating the discrepancy, I checked extracted files and found why different flag prefixes appeared during analysis:

- `r.0.-1.mca` modified time: 4/4/2026 8:16:48 PM
- `r.0.-1.mca.json` modified time: 4/4/2026 8:08:46 PM

This indicates the JSON dump was an older snapshot while the MCA region binary was newer.

Key point:
- Minecraft reads region binary (`.mca`) at runtime.
- `.mca.json` is a converted/exported copy and can be stale.

So the in-game value from MCA is the source of truth for the current world state. The prefix mismatch happened because JSON was outdated relative to the binary region data.

## Exploit (Explicit)

The exploit is **game-world clue extraction plus world-state manipulation**. The challenge relied on in-world placement and survival-state friction (dangerous spawn), but the save file could be inspected and adjusted using external tooling (`level.dat` edits), allowing reliable traversal and clue recovery.

## How I Did It

1. Identified the files as a Minecraft world save.
2. Imported the world and attempted exploration.
3. When the spawn loop blocked progress, edited `level.dat` with NBTExplorer to restore playable access.
4. Followed the in-world clue "Emreald Blocks are Beautiful" and searched that region.
5. Located the chest containing the flag.

## How to Prevent This

1. Design challenge logic expecting players may inspect or modify world metadata.
2. Avoid single-point progression blockers like lethal spawn loops.
3. Place critical secrets behind multiple validation conditions (not just discoverable map hints).
4. If external edits are considered out-of-scope, enforce server-side validation rather than offline world files.

## Takeaways
1. World-file recognition is crucial for non-traditional CTF challenges.
2. `level.dat` editing can recover soft-locked challenge states.
3. Always keep a clean backup of the original world before modifying or breaking structures.
4. I learned how to recover from accidental map damage and continue investigation safely by restoring known-good region data.
