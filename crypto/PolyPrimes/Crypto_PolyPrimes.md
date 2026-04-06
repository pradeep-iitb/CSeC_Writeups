# Crypto Challenge — PolyPrimes

## The Challenge Concept

This challenge uses a custom prime generation method based on polynomial equations and non-standard bases. Instead of standard RSA, the primes are built using a polynomial expansion where the coefficients come from randomly selecting which power terms to include.

Specifically:
- Each prime `p`, `q`, `r` is constructed as `p = 2 + sum of (0 or 1) * m^r` for various random power terms
- The base `m` and the power selections are kept secret
- The public key is `n = p * q * r`
- The ciphertext is computed using a modified exponent

The idea is that changing the representation base might somehow make it harder to factor, but as the challenge title hints, that does not actually work.

## My Initial Struggle

This was the hardest challenge for me to understand from a logic and code perspective. The polynomial reconstruction and constraint satisfaction involved was not straightforward.

I spent a lot of time trying to follow the math and grasp how the solve script actually recovered the prime factors from just the final modulus `n`.

## The Breakthrough with AI Assistance

At a certain point, I realized I needed help understanding the exact steps. That was when I worked with Claude to figure out:

1. How to convert `n` into digits in the unknown base to extract the polynomial structure
2. How the constraint satisfaction algorithm backtracks through digit choices to find which power terms were used
3. How to recover the individual primes `p`, `q`, `r` from the digit representation
4. How to compute Euler's totient and decrypt the ciphertext

The solve path involved roughly equal contributions: I understood the high-level flow and helped guide the logic, while Claude provided the detailed implementation and mathematical reasoning.

## How the Attack Works

1. Parse `n` and `c` from the output.
2. Convert `n` into digits in base 41 (the base used by the challenge).
3. Use backtracking recursion to recover which polynomial terms were used to build each prime.
4. Reconstruct `p`, `q`, `r` from the recovered polynomial coefficients.
5. Compute $\varphi(n) = (p-1)(q-1)(r-1)$.
6. Determine the public exponent `e` from the challenge parameters.
7. Compute the private exponent $d = e^{-1} \pmod{\varphi(n)}$.
8. Decrypt: `m = c^d mod n`.
9. Convert the result back to the flag format.

## Key Insight

The security flaw is that even though the primes are generated using a polynomial in a non-standard base, the digit representation of `n` in that base still leaks enough information to recover the structure. The base change does not provide real security.

## Exploit (Explicit)

The exploit is **structural leakage from custom prime generation**. The challenge tried to hide prime construction behind polynomial/base representation, but the final public modulus still leaked enough digit structure in that base to reconstruct factors.

## How to Prevent This

1. Use standard, reviewed key generation (well-tested RSA parameters) instead of custom polynomial prime schemes.
2. Avoid security-through-obscurity assumptions like "different base representation = harder factoring".
3. Validate new crypto constructions with formal analysis before deployment.

## Difficulties Faced

1. Understanding the algorithm logic was the hardest part for me.
2. It took significant time to understand how the polynomial terms mapped to actual prime reconstruction.
3. After finally understanding the core flow, I thought of a few possible solving directions and then used AI to complete the implementation details.

## What I Learned

1. Custom cryptography often fails by leaking structure unexpectedly.
2. The hardest part in crypto CTFs is often modeling and understanding the generation process, not the final decryption step.
3. AI can accelerate implementation, but only after the core logic is understood clearly.

## Result

Once the factorization logic was clear and implemented correctly, the rest was straightforward RSA decryption.

## Flag

`FLAG{Ch4nG1ng_7h3_8a5E_w0n7_m4Ke_1t_S4fe}`
