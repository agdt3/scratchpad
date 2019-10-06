%{
#define YYSTYPE double
#include <ctype.h>
#include <stdio.h>
#include <math.h>
%}

%token NUM

%%
input: /*empty*/ ;
input: input line ;
line: '\n' ;
line: exp '\n' { printf("\t%.10g\n", $1); } ;
exp: NUM ;
exp: '(' exp ')' { $$ = $2 } ;
exp: exp exp '+' { $$ = $1 + $2 } ;
exp: exp exp '-' { $$ = $1 - $2 } ;
exp: exp exp '*' { $$ = $1 * $2 } ;
exp: exp exp '/' { $$ = $1 / $2 } ;
exp: exp exp '^' { $$ = pow($1, $2) } ;
/*exp: exp '+' exp { $$ = $1 + $3 } ;*/
%%

yylex() {
  int c;
  while ((c = getchar()) == ' ' || c == '\t');

  if (c == '.' || isdigit(c)) {
    ungetc(c, stdin);
    scanf("%lf", &yylval);
    return NUM;
  }

  if (c == EOF) return 0;

  return c;
}

yyerror(s) {
  printf("%s\n", s);
}

main() {
  yyparse();
}
