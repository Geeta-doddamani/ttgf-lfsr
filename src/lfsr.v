/*
 * Copyright (c) 2024 Soumya Challagi
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_geeta_doddamani_lfsr (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path
    input  wire       ena,      // Enable
    input  wire       clk,      // Clock
    input  wire       rst_n     // Active-low reset
);

    reg  [3:0] lfsr;
    wire feedback;

    // 4-bit LFSR feedback
    // Polynomial: x^4 + x + 1
    assign feedback = lfsr[3] ^ lfsr[0];

    always @(posedge clk) begin
        if (!rst_n)
            lfsr <= 4'b0001;              // Seed value
        else
            lfsr <= {lfsr[2:0], feedback};
    end

    // 4-bit LFSR output is connected to lower 4 output pins
    assign uo_out[0] = lfsr[0];
    assign uo_out[1] = lfsr[1];
    assign uo_out[2] = lfsr[2];
    assign uo_out[3] = lfsr[3];

    // Upper 4 output pins are unused
    assign uo_out[4] = 1'b0;
    assign uo_out[5] = 1'b0;
    assign uo_out[6] = 1'b0;
    assign uo_out[7] = 1'b0;

    // Bidirectional IOs are not used
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Unused inputs to avoid warnings
    wire _unused = &{ena, ui_in, uio_in, 1'b0};

endmodule

`default_nettype wire
