
load Sort.asm,
output-file Sort-CHECK1.out,
compare-to Sort-CHECK1.cmp,
output-list RAM[0]%D1.6.1 RAM[1]%D1.6.1 RAM[2]%D1.6.1 RAM[3]%D1.6.1 RAM[4]%D1.6.1 RAM[5]%D1.6.1 RAM[6]%D1.6.1 RAM[7]%D1.6.1 RAM[8]%D1.6.1 RAM[9]%D1.6.1 RAM[10]%D1.6.1 RAM[11]%D1.6.1 RAM[12]%D1.6.1 RAM[13]%D1.6.1 RAM[14]%D1.6.1 RAM[15]%D1.6.1;

set RAM[11] 0,
set RAM[14] 11,
set RAM[15] 1;
repeat 30000 {
  ticktock;
}
output;


