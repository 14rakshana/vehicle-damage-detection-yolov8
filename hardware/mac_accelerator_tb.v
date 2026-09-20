`timescale 1ns/1ps

module mac_accelerator_tb;

    reg signed [7:0] a0, a1, a2, a3;
    reg signed [7:0] w0, w1, w2, w3;

    wire signed [19:0] result;

    mac_accelerator dut (
        .a0(a0),
        .a1(a1),
        .a2(a2),
        .a3(a3),
        .w0(w0),
        .w1(w1),
        .w2(w2),
        .w3(w3),
        .result(result)
    );

    initial begin

        // Test case:
        // 2*3 + 4*5 + 1*2 + 3*4 = 40

        a0 = 2;
        a1 = 4;
        a2 = 1;
        a3 = 3;

        w0 = 3;
        w1 = 5;
        w2 = 2;
        w3 = 4;

        #10;

        $display("MAC Result = %d", result);

        if (result == 40)
            $display("TEST PASSED");
        else
            $display("TEST FAILED");

        $finish;
    end

endmodule