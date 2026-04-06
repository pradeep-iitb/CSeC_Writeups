# Web Challenge 2 — What The Book

## Architecture of the Website

This challenge was a small online bookstore built on **Express** running over **Bun**, with an **in-memory SQLite** database.

The architecture was pretty straightforward:
- The app loaded all book metadata from `books.json`.
- User accounts and sessions were stored in SQLite.
- The homepage was served as static frontend content.
- The cart logic lived on the backend through `/cart/add` and `/cart/checkout`.
- Checkout bundled the selected book files into a ZIP archive and returned it to the user.

The important part was that the application trusted backend-side price calculations too much and relied on JavaScript arithmetic with mixed data types.

## Absurd Datatype for Prices

While reviewing `books.json`, I noticed something unusual: one of the book prices was not stored as a number.

- Most books had numeric prices like `20` or `40`.
- But one entry had the price stored as the string `"10"`.

That looked harmless at first, but in JavaScript it becomes a problem because `+` behaves differently depending on whether the operands are numbers or strings. That meant the cart total could drift into string concatenation instead of proper numeric addition.

This number-format inconsistency (misformatted numeric field) was the core weakness.

## What I Tried First
I first focused on straightforward application-logic testing, since this was a pure web challenge.

My next idea was to bundle the flag book together with other normal books and see whether the total calculation would behave strangely enough to allow it. That approach did not work reliably on its own, because the price check still blocked direct over-budget additions.

The hardest part was realizing the exploit only worked reliably when adding both relevant books together in a single crafted API request.

## Why the Script Worked

The exploit script solved the issue by sending the cart items in one carefully crafted request instead of adding them manually one by one.

The key idea was this:

1. Register a new user to get a valid session cookie.
2. Send `/cart/add` with **two products in the same request**:
  - the cheap book with the string price `"10"`
  - the flag book
3. Because the first price was a string, the `reduce()` used for `additionalSum` could switch into string concatenation mode.
4. The backend also pulled the current cart sum from the database, and on an empty cart that value was `NULL`.
5. When the backend evaluated the budget check, the mixed-type expression no longer behaved like a clean numeric comparison, so the insufficient-funds check was bypassed.
6. After that, `/cart/checkout` returned a ZIP archive containing the selected files, including `flag.txt`.

So the exploit was not about manually forcing the cart through the UI. It was about using the API directly and abusing the backend's type confusion in the total calculation.

## Exploit (Explicit)

The exploit is **type confusion caused by mixed numeric/string price values and null handling in cart total logic**, enabling a budget-check bypass when request payload is crafted correctly.

## How to Prevent This

1. Enforce strict schema validation (all prices must be numeric) at ingestion time.
2. Use consistent numeric types in database and application code.
3. Never rely on JavaScript implicit coercion for security-critical comparisons.
4. Normalize null sums to `0` explicitly before arithmetic.
5. Add server-side invariant checks and tests for mixed-type and edge-case payloads.

## What I Learned

1. Small data-format inconsistencies can become full authorization/budget bypasses.
2. API-level crafted requests can trigger logic paths that UI testing misses.
3. Type-safe validation and explicit coercion rules are essential in web backends.

## Result

Using the script, I was able to:
- create a session,
- bypass the cart price restriction,
- checkout the flag book,
- and extract the flag from the downloaded ZIP.

## Flag

CSeC{po0R_C0nC4TEN4T10N}
