// Simple AXIS FIFO. Not piplined (s_ready = m_ready)
`timescale 1ns/1ps

module axis_fifo #(
  parameter WIDTH=8,
  parameter DEPTH=4
)(
    input  logic aclk, aresetn, 

    output logic s_ready,
    input  logic s_valid,
    input  logic s_last, 
    input  logic [WIDTH   -1:0] s_data,
    input  logic [WIDTH/8 -1:0] s_keep,

    input  logic m_ready,
    output logic m_valid,
    output logic m_last, 
    output logic [WIDTH   -1:0] m_data,
    output logic [WIDTH/8 -1:0] m_keep
);

`ifdef COCOTB_SIM
  initial begin
    $dumpfile ("axis_fifo.vcd");
    $dumpvars (0, axis_fifo);
    #1;
  end
`endif

  localparam WIDTH_ALL = WIDTH + WIDTH/8 + 2;
  logic [DEPTH-1:0][WIDTH_ALL-1:0] data_in ;
  logic [DEPTH-1:0][WIDTH_ALL-1:0] data_out;

  assign data_in[0] = {s_data, s_valid, s_keep, s_last};

  genvar i;
  for (i=1; i<DEPTH; i=i+1)
    assign data_in[i] = data_out[i-1];

  always @(posedge aclk or negedge aresetn)
    if      (~aresetn) data_out  <= '0;
    else if (m_ready ) data_out  <= data_in;

  assign {m_data, m_valid, m_keep, m_last} = data_out[DEPTH-1];
  assign s_ready = m_ready;

endmodule