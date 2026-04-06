from math import gcd

n = 175825434991812844002856796848007783718030968597274659260989246756308541475259564155604299796921869318388524974905021729012515713190313131952474546262634475838277955781683097979024117896291625600596443338955020502184760949797964767911000375129211387920159130242975137648401360380899816242351853003748453397369311278359169015391614374421588245041509271214231826585723078309817150377462722683226152931996718994192346388801610612908655419376532897978665831255383819221018804223716491865110156556793035529417614400950429444546535306532391138828129365836926069364950556668695196102952792321882131713466275441013499993
c = 25091401983042066844957599555336836765377101938707753294037019168061180977556178877818537194307056693879629173723442858033738087161776559394151880175810358930243472960524106477097258623692682764310051984226564804744110027142739627480159802511560985119338863552814483526101165862758488283270267532936675861534058504176846364257186211864087132187010085742398933804204637457480165260467349482794355413203528837996868301881123796747762734360541014330471502919483189956560426385214416961111427848077903532638211999433875049440616527767072059109210792663748862284075932734680839846173335126372442911581698972329718849

BASE = 41
MAX_EXP = 149
MAX_K = 3 * MAX_EXP


def long_to_bytes(x: int) -> bytes:
    if x == 0:
        return b"\x00"
    return x.to_bytes((x.bit_length() + 7) // 8, "big")


def to_base_digits(x: int, base: int) -> list[int]:
    out = []
    while x:
        out.append(x % base)
        x //= base
    return out


def from_base_digits(digits: list[int], base: int) -> int:
    val = 0
    p = 1
    for d in digits:
        val += d * p
        p *= base
    return val


def recover_factors() -> tuple[int, int, int]:
    nd = to_base_digits(n, BASE)
    if len(nd) < MAX_K + 2:
        nd += [0] * (MAX_K + 2 - len(nd))

    a = [0] * (MAX_EXP + 1)
    b = [0] * (MAX_EXP + 1)
    r = [0] * (MAX_EXP + 1)
    a[0] = b[0] = r[0] = 2

    # Small branching set for triples whose bit-sum is fixed.
    combos_by_sum = {
        0: [(0, 0, 0)],
        1: [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
        2: [(1, 1, 0), (1, 0, 1), (0, 1, 1)],
        3: [(1, 1, 1)],
    }

    def coeff_k(k: int, upto: int) -> int:
        total = 0
        hi_i = min(k, upto)
        for i in range(0, hi_i + 1):
            ai = a[i]
            if ai == 0:
                continue
            hi_j = min(k - i, upto)
            for j in range(0, hi_j + 1):
                bj = b[j]
                if bj == 0:
                    continue
                l = k - i - j
                if 0 <= l <= upto:
                    rv = r[l]
                    if rv:
                        total += ai * bj * rv
        return total

    def verify_suffix(start_idx: int, carry_in: int) -> bool:
        carry = carry_in
        for k in range(start_idx + 1, MAX_K + 1):
            s = coeff_k(k, start_idx)
            num = carry + s - nd[k]
            if num % BASE != 0:
                return False
            carry = num // BASE
            if carry < 0:
                return False
        return carry == 0

    # k = 0 equation gives initial carry.
    init_num = coeff_k(0, 0) - nd[0]
    if init_num % BASE != 0:
        raise ValueError("Invalid base assumption")
    init_carry = init_num // BASE

    solved = False
    nodes = 0

    def dfs(cur_idx: int, carry_in: int) -> bool:
        nonlocal solved, nodes
        if solved:
            return True
        nodes += 1

        if cur_idx == MAX_EXP:
            if verify_suffix(cur_idx, carry_in):
                solved = True
                return True
            return False

        nxt = cur_idx + 1
        base_part = coeff_k(nxt, cur_idx)

        # At position nxt, unknown bits only affect coefficient by 4 * (x+y+z).
        for bit_sum in (0, 1, 2, 3):
            num = carry_in + base_part + 4 * bit_sum - nd[nxt]
            if num % BASE != 0:
                continue
            carry_out = num // BASE
            if carry_out < 0:
                continue

            for av, bv, rv in combos_by_sum[bit_sum]:
                a[nxt], b[nxt], r[nxt] = av, bv, rv
                if dfs(nxt, carry_out):
                    return True
                a[nxt], b[nxt], r[nxt] = 0, 0, 0

        return False

    if not dfs(0, init_carry):
        raise RuntimeError("Could not reconstruct factors")

    p = from_base_digits(a, BASE)
    q = from_base_digits(b, BASE)
    rr = from_base_digits(r, BASE)

    if p * q * rr != n:
        raise RuntimeError("Factor reconstruction check failed")

    print(f"Recovered factors via structural leakage in {nodes} nodes")
    return p, q, rr


def decrypt_flag(p: int, q: int, r: int) -> bytes:
    phi = (p - 1) * (q - 1) * (r - 1)

    # z cannot be directly recovered from coefficients because generator also
    # injected hidden zero-choices. Restrict search to mathematically valid range.
    lower_z = max(
        sum(1 for x in to_base_digits(p, BASE)[1:] if x),
        sum(1 for x in to_base_digits(q, BASE)[1:] if x),
        sum(1 for x in to_base_digits(r, BASE)[1:] if x),
    )

    for z in range(lower_z, 150):
        e = BASE**3 + z - 2
        if gcd(e, phi) != 1:
            continue
        d = pow(e, -1, phi)
        pt = long_to_bytes(pow(c, d, n))
        if b"FLAG{" in pt and pt.rstrip().endswith(b"}"):
            print(f"Recovered z = {z}")
            return pt

    raise RuntimeError("Could not recover plaintext")


def solve() -> None:
    p, q, r = recover_factors()
    flag = decrypt_flag(p, q, r)
    print(flag.decode(errors="replace"))


if __name__ == "__main__":
    solve()
