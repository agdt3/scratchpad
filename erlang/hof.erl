-module(hof).
-compile(export_all).

one() -> 1.
two() -> 2.
add(X, Y)
  -> X() + Y().

increment(V) -> V + 1.
map(_, []) -> [];
map(F, [H|T]) -> [F(H)|map(F, T)].

tail_map(_, []) -> [];
tail_map(F, List) -> tail_map(F, List, []).
tail_map(F, [H|T], Acc) -> tail_map(F, T, [F(H)|Acc]);
tail_map(_, [], Acc) -> Acc.

filter(_, []) -> [];
filter(Pred, List) -> filter(Pred, List, []).
filter(_, [], Acc) -> Acc;
filter(Pred, [H|T], Acc) ->
  case Pred(H) of
    true -> filter(Pred, T, [H|Acc]);
    false -> filter(Pred, T, Acc)
  end.

sum(List) -> sum(List, 0).
sum([H|T], Acc) -> sum(T, H + Acc);
sum([], Acc) -> Acc.

fold_max([H|T]) -> fold_max2(T, H).
fold_max2([], Max) -> Max;
fold_max2([H|T], Max) when H > Max -> fold_max2(T, H);
fold_max2([H|T], Max) when H =< Max -> fold_max2(T, Max).

foldr(_, []) -> [].
foldr(_, [], Acc) -> Acc;
foldr(F, [H|T], Acc) -> foldr(F, T, F(H, Acc)).

reverse(List) ->
  foldr(fun(X, Acc) -> [X|Acc] end, List, []).

map2(F, List) ->
  foldr(F, List, []).
