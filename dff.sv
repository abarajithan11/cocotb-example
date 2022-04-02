// dff.sv
`timescale 1us/1ns

module dff (
    input  logic clk, 
    input  logic [7:0] d,
    output logic [7:0] q
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