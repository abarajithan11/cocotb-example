// dff.sv
`timescale 1us/1ns

module dff #(
  parameter WIDTH_IN=8,
  parameter WIDTH_OUT=8
)(
    input  logic clk, 
    input  logic [WIDTH_IN -1:0] d,
    output logic [WIDTH_OUT-1:0] q
);

`ifdef COCOTB_SIM
initial begin
  $dumpfile ("dff.vcd");
  $dumpvars (0, dff);
  #1;
end
`endif

always @(posedge clk)
    q <= d;

endmodule