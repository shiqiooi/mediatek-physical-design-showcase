module counter8 #(
    parameter WIDTH = 8
)(
    input wire clk,
    input wire rst,
    input wire en,
    output reg [WIDTH-1:0] count,
    output wire terminal_count
);

always @(posedge clk) begin
    if (rst)
        count <= {WIDTH{1'b0}};
    else if (en)
        count <= count + 1'b1;
end

assign terminal_count = (count == {WIDTH{1'b1}});

endmodule
