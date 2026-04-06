# Forensics Challenge — Bald Boy

## The Challenge

A user is searching for a lost Amazon order ID in their Outlook inbox. The challenge provides `challenge.pcap` (network capture)  to help locate the missing ID. The flag format is: `CSeC{XXX-XXXXXXX-XXXX}` .

The challenge statement hints at Outlook, but that's misdirection. The real data is in the network traffic captured in the PCAP.

## My Investigation Journey

### Phase 1: Initial Exploration & Endpoint Discovery

I opened the PCAP in Wireshark and started with logical endpoint guessing:
- Searched for e-commerce endpoints: `/books`, `/profile`, `/cart`, `/track-order`, `/account/orders`
- Applied HTTP filters to identify all POST and GET requests
- Checked for order-related keywords in traffic

These endpoint names (`/track-order`, `/account/orders`) reinforced the order tracking theme and suggested the data was related to e-commerce/order management.

However, endpoint discovery alone didn't lead to the flag. I also tried advanced forensics techniques without success:
- IP header steganography
- TCP sequence number patterns
- TTL-based encoding

### Phase 2: The Bearer Token Discovery

While systematically reviewing packets, I found something suspicious:

**POST request with Authorization header:**
```
POST /exfil HTTP/1.1
Authorization: Bearer TXlBbWF6b25vcmRlcmlk
```

I searched for type of encoding & Base64 decoded the bearer token:
```
Input:  TXlBbWF6b25vcmRlcmlk
Output: MyAmazonorderid
```

This was the **breakthrough clue**: the token literally names the artifact—"MyAmazonorderid". Data exfiltration of an Amazon order ID.

### Phase 3: Navigating Deliberate Decoys

The PCAP contained intentional distractions:
- **Fake hex values**: `0xBEEF`, `0xCAFE`, `0xDEAD`, `0xCOFFEE`, `0xFACE`
- **False flags** in HTML comments
- **Misleading order ID candidates** in incorrect format variations

The challenge wasn't obvious; it required filtering signal from noise.

### Phase 4: Manual Breakthrough

When pattern-matching hit dead ends, I switched to reading packets **chronologically from the beginning** instead of searching for keywords.

Following the user's browsing journey revealed:
- Multiple HTTP requests to different domains
- Navigation to **Inscryption** (discoverablr  as an online game website)
- Within the site, an **order confirmation page**
- The actual order ID embedded in the website content

### Phase 5: Validation

Verified the order ID:
- Matched the challenge format `CSeC{XXX-XXXXXXX-XXXX}`
- Realistic Amazon order ID format 
- Cross-referenced against false candidates

## Why This Took Time

The answer required understanding the **user's narrative** (where they browsed) rather than isolated packet inspection. Professional decoys and thousands of packets made systematic analysis necessary.

I had to search through packets repeatedly and deeply before finding the real signal.

## Exploit (Explicit)

The exploit is **traffic-level data exfiltration hidden among decoys**. Sensitive order information was exposed through observable HTTP traffic and contextual browsing traces, while fake indicators were inserted to waste analyst time.

## How to Prevent This

1. Enforce HTTPS/TLS everywhere to reduce plaintext leakage in captures.
2. Prevent sensitive identifiers from being exposed in unnecessary requests or logs.
3. Monitor and alert on suspicious exfiltration endpoints and unusual authorization tokens.

## What I Learned

1. Deep packet analysis is often about timeline reconstruction, not only keyword search.
2. Decoys can be beaten by methodical chronological review.
3. I learned new practical packet-forensics concepts while validating signal vs noise.

## Flag

`CSeC{602-2548141-2180332}` 

Format note: The extracted Amazon order ID was `CSeC{602-2548141-2180332}`, but per the challenge-required format `CSeC{XXX-XXXXXXX-XXXX}`, the submitted flag is `CSeC{602-2548141-2180}`.
