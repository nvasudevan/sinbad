%{
#include "yygrammar.h"
%}
%%
"a"    { return 'a'; }
"b"    { return 'b'; }
"c"    { return 'c'; }
"d"    { return 'd'; }
"e"    { return 'e'; }
"f"    { return 'f'; }
"g"    { return 'g'; }
"h"    { return 'h'; }
"i"    { return 'i'; }
"j"    { return 'j'; }
"k"    { return 'k'; }
"l"    { return 'l'; }
"m"    { return 'm'; }
"n"    { return 'n'; }
"o"    { return 'o'; }
"p"    { return 'p'; }
"q"    { return 'q'; }
"r"    { return 'r'; }
"s"    { return 's'; }
"t"    { return 't'; }
"u"    { return 'u'; }
"v"    { return 'v'; }
"w"    { return 'w'; }
"x"    { return 'x'; }
"y"    { return 'y'; }
"z"    { return 'z'; }
" "    { /* skip blank */ }
\n     { yypos++; /* adjust linenumber and skip newline */ }
.      { yyerror("illegal token"); }
