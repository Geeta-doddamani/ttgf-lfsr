/*
 * Copyright (c) 2024 Geeta Doddamani
 * SPDX-License-Identifier: Apache-2.0
 *
 * 4-bit Maximum-Length LFSR
 *
 * Feedback polynomial: x^4 + x + 1  (taps at bits 3 and 0)
 * Left-shift topology: lfsr <= {lfsr[2:0], lfsr[3]^lfsr[0]}
 * Seed on reset: 4'b0001 (0x1)
 *
 * Expected sequence (period = 15):
 *   1->3->7->F->E->D->A->5->B->6->C->9->2->4->8->(repeat)
 *
 * Pin mapping:
 *   uo_out[3:0] = LFSR output (lower nibble)
 *   uo_out[7:4] = 0 (unused, tied low)
 *   uio_out     = 0
 *   uio_oe      = 0
 */

`default_nettype none

module tt_um_geeta_doddamani_lfsr (
    input  wire [7:0] ui_in,    // Dedicated inputs  (unused)
    output wire [7:0] uo_out,   // Dedicated outputs: uo_out[3:0] = LFSR, [7:4] = 0
    input  wire [7:0] uio_in,   // IOs: Input path   (unused)
    output wire [7:0] uio_out,  // IOs: Output path  (tied to 0)
    output wire [7:0] uio_oe,   // IOs: Enable path  (all inputs)
    input  wire       ena,      // Always 1 when powered
    input  wire       clk,      // Clock
    input  wire       rst_n     // Active-low reset
);

  // 4-bit LFSR register
  reg [3:0] lfsr;

  // Feedback bit: taps at positions 3 and 0  (x^4 + x + 1)
  wire feedback = lfsr[3] ^ lfsr[0];

  always @(posedge clk) begin
    if (!rst_n) begin
      lfsr <= 4'b0001;                    // seed = 0x1 on reset
    end else begin
      lfsr <= {lfsr[2:0], feedback};      // left-shift with feedback into LSB
    end
  end

  // Output: lower nibble = LFSR, upper nibble forced to 0
  assign uo_out  = {4'b0000, lfsr};

  // Bidirectional IOs unused
  assign uio_out = 8'b0;
  assign uio_oe  = 8'b0;

  // Suppress unused-input warnings
  wire _unused = &{ena, ui_in, uio_in, 1'b0};

endmodule
