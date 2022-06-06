// register.sv
`timescale 1us/1ns

module register #(
  parameter WIDTH_IN=8,
            WIDTH_OUT=8
)(
    input  logic clk, 
    input  logic [WIDTH_IN -1:0] d,
    output logic [WIDTH_OUT-1:0] q
);

always @(posedge clk) // iverilog linux doesn't support always_ff
    q <= d;


`ifdef COCOTB_SIM
initial begin
  $dumpfile ("register.vcd"); $dumpvars;
end
`endif

endmodule