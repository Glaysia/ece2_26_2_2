module full_adder(input wire a,b,cin, output wire s,cout);
  wire partial_sum, carry_ab, carry_cin;
  half_adder first(a,b,partial_sum,carry_ab);
  half_adder second(partial_sum,cin,s,carry_cin);
  assign cout = carry_ab | carry_cin;
endmodule
