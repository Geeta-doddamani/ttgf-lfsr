`timescale 1ns/1ps

module lfsr_4bit(
    input  wire clk,
    input  wire reset,
    output reg  [3:0] lfsr
);

wire feedback;

assign feedback = lfsr[3] ^ lfsr[0];

always @(posedge clk) begin
    if (reset)
        lfsr <= 4'h1;          // Seed value = 0001
    else
        lfsr <= {lfsr[2:0], feedback};
end

endmodule
