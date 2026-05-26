/* block comment */
// multi line comment part 1
// multi line comment part 2
grammar Sample;

start: ID EOF;
ID: [a-zA-Z]+; // single line comment
WS: [ \t\r\n]+ -> skip;
