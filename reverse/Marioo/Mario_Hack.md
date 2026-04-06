# Reverse Challenge - Mario

## Challenge Context

The challenge required completing a custom World 8-4 build distributed in `reverse/Marioo/dist/dist/uMario-2`. The hint explicitly mentioned Cheat Engine, so the intended path was not only gameplay skill but runtime analysis and memory manipulation.

Because of that hint, I approached it like a reverse-engineering task over a running process: identify critical gameplay variables in RAM, understand which ones are authoritative, and bypass state transitions that enforce failure.

## Tooling and Setup

I first studied Cheat Engine basics using Google and YouTube so I could apply the correct scan pipeline instead of random value edits. Then I:

1. Launched the game.
2. Attached Cheat Engine to the game process.
3. Started with standard, easy-to-verify fields (timer/lives) to confirm that reads and writes worked.

This calibration phase was useful because it verified three things:

- the process attachment was correct,
- datatype assumptions were workable,
- and freeze operations were taking effect when the address was truly writable and not immediately overwritten.

## Unknown Initial Value Workflow

The main challenge was not reading known values, but finding unknown internal state flags. I used the classic unknown-initial-value narrowing strategy:

1. Begin with unknown initial value.
2. Trigger controlled in-game actions.
3. Filter by increased, decreased, changed, and unchanged.
4. Repeat until candidate addresses dropped to a manageable set.

The key to reducing false positives was controlled action design:

- stand still versus move,
- jump versus no jump,
- touch hazard versus avoid hazard,
- and compare resulting scan deltas.

This made it possible to separate movement-related addresses from state-machine addresses.

## Coordinates vs State Variables

My first idea was coordinate manipulation (teleport style). That partially worked, but it was noisy because many addresses mirrored position, velocity, animation or camera offsets. Editing one coordinate-like value often gave unstable behavior or had no lasting impact.

I then shifted focus from position to game logic state, especially variables related to:

- death/game-over handling,
- Mario state transitions (normal jump, slide, big Mario, big Mario jump, swim),
- orientation/facing bits,
- and Y-axis behavior around hazards.

This direction was more reliable because these variables govern how the engine interprets collisions, not just where the sprite appears.

## Why Freeze Alone Was Not Enough

I froze several candidate values, including game-over related flags and Mario state values. However, when touching fire bars, some values changed for milliseconds and then reverted.

Important observation:

- There was no full game-over screen.
- Mario's death animation still triggered (short downward fall).
- If another fire bar was not touched immediately, the game could return to normal.

This indicated I was blocking part of the fail pipeline (level reload), but not the animation/death trigger itself. In technical terms, I was suppressing one downstream effect while the upstream state transition still fired.

## Instruction-Level Intervention

After seeing values revert quickly, I inspected the write path using the Cheat Engine feature that shows what accesses or writes to an address. That revealed active code paths reapplying state updates.

At this point, I moved from value freezing to instruction patching:

1. Locate the instruction writing the problematic state.
2. Patch that instruction to a no-op style behavior (do nothing).
3. Re-test hazard interaction.

This prevented the game from repeatedly forcing the unwanted state. Conceptually, this is stronger than freezing because it removes the source of the write rather than fighting its effect frame by frame.

## Instability and Crash Cases

During experimentation, not all edits were safe. Two common failure modes occurred:

- writing arbitrary values to unstable runtime fields,
- patching frequently executed instructions that had broader side effects.

Both led to glitches or crashes, requiring restart and re-validation. The fix was to keep edits minimal and only patch values/instructions that were repeatedly verified.

## Final Solve Path

I eventually reached endgame using controlled memory manipulation:

- freeze/selectively manipulate game-over and state-related variables,
- keep Y-coordinate handling favorable to bypass hazard-heavy sections,
- avoid over-patching unrelated logic,
- then complete the final segment and defeat the dragon.

I also attempted direct coordinate forcing and replacing every changing variable with no-op to reach the princess earlier, but that did not trigger success reliably. The stable solve came from preserving enough normal game logic while only bypassing the failure-critical parts.

Once the level completion condition was satisfied correctly, the challenge output string was recovered.

## Technical Takeaways

1. For Game challenges, unknown-value scan discipline matters more than random memory edits.
2. Position values are often decoys ; state-machine variables are usually more important.
3. Freeze-only strategies fail when the game has frequent manipulations .
4. Patching the writer instruction can be more robust at the same time complex than fighting repeated memory updates.
5. Minimal, validated patches are safer than broad edits in hot code paths .

## Flag

CSeC{NO-H4CK5-TH15-T1M3?}
