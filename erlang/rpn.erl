-module(rpn).
-compile(export_all).

% Token list, operation stack
rpn(L) when is_list(L) ->
  [Res] = lists:foldl(fun rpn/2, [], string:tokens(L, " ")),
  Res.

rpn("/", [N1,N2|S]) -> [N2 / N1|S];
rpn("*", [N1,N2|S]) -> [N2 * N1|S];
rpn("+", [N1,N2|S]) -> [N2 + N1|S];
rpn("-", [N1,N2|S]) -> [N2 - N1|S];
rpn("^", [N1,N2|S]) -> [math:pow(N2,N1)|S];
rpn("ln", [N|S])    -> [math:log(N)|S];
rpn("log10", [N|S]) -> [math:log10(N)|S];
rpn("sum", Stack) ->
  Res = lists:foldl(fun(X, Acc) -> X + Acc end, 0, Stack),
  [Res];
rpn("prod", Stack) ->
  Res = lists:foldl(fun(X, Acc) -> X * Acc end, 1, Stack),
  [Res];
rpn(X, Stack) -> [read(X)|Stack].


read(N) ->
  case string:to_float(N) of
    {error,no_float} -> list_to_integer(N);
    {F,_} -> F
  end.
