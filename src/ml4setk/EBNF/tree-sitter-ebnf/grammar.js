module.exports = grammar({
  name: 'EBNF',

  extras: $ => [/\s+/],

  conflicts: $ => [[$.sequenceNoSelection]],

  rules: {

    source_file: $ => repeat($.rule),

    rule: $ => seq($.lhs, '::=', $.rhs, ';'),
    lhs: $ => $.identifier,

    rhs: $ => choice(
      $.set,
      seq($.sequence, repeat(seq('|', $.sequence)))
    ),

    set: $ => seq('{', repeat(choice($.identifier, $.terminal, $.regex)), '}'),

    sequence: $ => seq($.statements, repeat($.statements)),

    statements: $ => prec(2, choice(
      $.quantifiedStatement,
      $.parenthesizedStatement,
      $.terminal,
      $.identifier,
      $.regex
    )),

    quantifiedStatement: $ => seq($.quantifierBase, choice('+', '*', '?')),
    quantifierBase: $ => choice($.parenthesizedStatement, $.identifier, $.terminal, $.regex),

    parenthesizedStatement: $ => seq('(', $.sequence, ')'),

    sequenceNoSelection: $ => repeat1($.statementsNoSelection),
    statementsNoSelection: $ => choice(
      $.quantifiedStatement,
      $.parenthesizedStatement,
      $.terminal,
      $.identifier,
      $.regex
    ),

    terminal: $ => seq("'", $.stringContent, "'"),
    stringContent: $ => /[^']*/,

    regex: $ => token(seq(
      '/',
      repeat(choice(
        /[^/\\]/,
        seq('\\', /./)
      )),
      '/'
    )),
    identifier: _ => /[_A-Za-z][_A-Za-z0-9]*/
  }
});
