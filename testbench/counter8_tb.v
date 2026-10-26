`timescale 1ns/1ps

module counter8_tb;

reg clk = 0;
reg rst = 0;
reg en = 0;

wire [7:0] count;
wire terminal_count;

integer errors = 0;
integer checks = 0;
integer i;

counter8 #(.WIDTH(8)) dut (
    .clk(clk),
    .rst(rst),
    .en(en),
    .count(count),
    .terminal_count(terminal_count)
);

// Generate a clock with 10 ns period
always #5 clk = ~clk;

// Compare actual outputs with expected outputs
task check;
    input [7:0] expected_count;
    input expected_tc;
    begin
        checks = checks + 1;
        if (count !== expected_count ||
            terminal_count !== expected_tc) begin
            $display("FAIL check=%0d: count=%0d expected=%0d TC=%b expected_TC=%b",
                     checks, count, expected_count,
                     terminal_count, expected_tc);
            errors = errors + 1;
        end
    end
endtask

task step;
    input reset_value;
    input enable_value;
    input [7:0] expected_count;
    input expected_tc;
    begin
        @(negedge clk);
        rst = reset_value;
        en = enable_value;

        @(posedge clk);
        #1;
        check(expected_count, expected_tc);
    end
endtask

initial begin
    $dumpfile("counter8.vcd");
    $dumpvars(0, counter8_tb);

    $display("Starting Counter8 Functional Verification");

    // TC01: Synchronous reset
    step(1, 0, 0, 0);

    // TC02: Counting from 0 to 5
    for (i = 1; i <= 5; i = i + 1)
        step(0, 1, i, 0);

    // TC03: Hold count at 5
    step(0, 0, 5, 0);
    step(0, 0, 5, 0);

    // TC04: Reset priority
    step(1, 1, 0, 0);

    // TC05: Count to terminal value 255
    for (i = 1; i <= 255; i = i + 1)
        step(0, 1, i, (i == 255));

    // TC06: Hold at terminal count
    step(0, 0, 255, 1);

    // TC07: Wraparound from 255 to 0
    step(0, 1, 0, 0);

    if (errors == 0)
        $display("ALL TESTS PASSED (%0d checks)", checks);
    else
        $fatal(1, "TEST FAILED: %0d errors", errors);

    $finish;
end

endmodule
