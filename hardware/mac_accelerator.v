module mac_accelerator (
    input  signed [7:0]  a0,
    input  signed [7:0]  a1,
    input  signed [7:0]  a2,
    input  signed [7:0]  a3,

    input  signed [7:0]  w0,
    input  signed [7:0]  w1,
    input  signed [7:0]  w2,
    input  signed [7:0]  w3,

    output signed [19:0] result
);

    wire signed [15:0] mult0;
    wire signed [15:0] mult1;
    wire signed [15:0] mult2;
    wire signed [15:0] mult3;

    assign mult0 = a0 * w0;
    assign mult1 = a1 * w1;
    assign mult2 = a2 * w2;
    assign mult3 = a3 * w3;

    assign result = mult0 + mult1 + mult2 + mult3;

endmodule