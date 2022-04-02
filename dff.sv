// dff.sv
`timescale 1us/1ns

module dff (
    output logic q,
    input logic clk, d
);

`ifdef COCOTB_SIM
initial begin
  $dumpfile ("dff.vcd");
  $dumpvars (0, dff);
  #1;
end
`endif

always @(posedge clk) begin
    q <= d;
end

endmodule