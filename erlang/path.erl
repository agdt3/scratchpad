-module(path).
-compile(export_all).

main() ->
  {ok, Binary} = file:read_file("road.txt"),
  Items = parse_map(Binary),
  group_vals(Items).

parse_map(Bin) when is_binary(Bin) ->
  parse_map(binary_to_list(Bin));
parse_map(StrList) when is_list(StrList) ->
  [list_to_integer(X) || X <- string:tokens(StrList, "\r\n\t ")].

group_vals(List) -> group_vals(List, []).
group_vals([], Acc) -> lists:reverse(Acc);
group_vals([A,B,X|Rest], Acc) -> group_vals(Rest, [{A,B,X}|Acc]).

search(List) -> search(List, [{0, []}, {0, []}]).
search([], Acc) ->
  io:format("~w~n", [Acc]),
  Acc;
search([{A,B,X}|T], [{DistA, PathA}, {DistB, PathB}]) ->
  case {A,B,X} of
    {A,B,X} when A + DistA =< (B + X) -> PathToA = {A + DistA, A};
    {A,B,X} when (B + X + DistA) < A -> PathToA = [B,X];
    _ -> PathToA = []
  end,
  case {A,B,X} of
    {A,B,X} when B =< (A+X) -> PathToB = [B];
    {A,B,X} when (A + X) < B -> PathToB = [A,X];
    _ -> PathToB = []
  end,
  search(T, [PA ++ PathToA, PB ++ PathToB]).
