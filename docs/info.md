<!---
This file is used to generate your project datasheet.
-->

## How it works

This project implements a **4-bit Maximum-Length Linear Feedback Shift Register (LFSR)** using the feedback polynomial **x⁴ + x + 1** (taps at bit positions 3 and 0).

On every rising clock edge the register shifts left by one position and a new feedback bit — computed as the XOR of bits 3 and 0 — is inserted at the LSB. When the active-low reset (`rst_n`) is asserted the register is loaded with the seed value `0x1`.

Because the polynomial is primitive, the LFSR cycles through all **15 non-zero 4-bit states** before repeating:

```
1 → 3 → 7 → F → E → D → A → 5 → B → 6 → C → 9 → 2 → 4 → 8 → (repeat)
```

The 4-bit LFSR value is driven out on `uo_out[3:0]`. The upper nibble `uo_out[7:4]` is always zero. All bidirectional IOs (`uio_out`, `uio_oe`) are also held at zero; no input pins are used.

## How to test

1. Assert reset by driving `rst_n = 0` for at least 2 clock cycles. After reset, `uo_out[3:0]` should read `0x1`.
2. Release reset (`rst_n = 1`). On each subsequent rising clock edge the output advances through the pseudo-random sequence: `1 → 3 → 7 → F → E → D → A → 5 → B → 6 → C → 9 → 2 → 4 → 8`, then repeats.
3. Verify `uo_out[7:4]` remains `0x0` at all times.
4. Verify `uio_out` and `uio_oe` remain `0x00` at all times.
5. After 15 clock cycles the output should return to `0x1`, confirming the full maximum-length period.

## External hardware

None required. The design is fully self-contained and needs only a clock and reset signal.
