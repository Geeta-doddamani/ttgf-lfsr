`timescale 1ns/1ps

module lfsr_tb;

reg clk, reset;
wire [3:0] lfsr_out;

lfsr_4bit DUT (
    .clk(clk),
    .reset(reset),
    .lfsr(lfsr_out)
);

initial begin
    clk = 0;
    forever #5 clk = ~clk;   // 100 MHz clock
end

initial begin
    reset = 1;
    #20 reset = 0;

    #200 $finish;
end

initial begin
    $monitor("Time=%0t | clk=%b | reset=%b | lfsr_out=%b",
              $time, clk, reset, lfsr_out);
end

endmodule
