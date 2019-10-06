-module(recursion).
-compile(export_all).

fact(0)
  -> 1;
fact(N) when N > 0
  -> N * fact(N-1).

fact_tail(N) -> fact_tail(N, 1).

fact_tail(1, Acc) -> Acc;
fact_tail(N, Acc) -> fact_tail(N - 1, N * Acc).

len([]) -> 0;
len([_|T]) -> 1 + len(T).

len_tail(L) -> len_tail(L, 0).
len_tail([], Acc) -> Acc;
len_tail([_|T], Acc) -> len_tail(T, Acc+1).

reverse([]) -> [];
reverse([H|T]) -> reverse(T) ++ [H].

reverse_tail(List) -> reverse_tail(List, []).
reverse_tail([], Acc) -> Acc;
reverse_tail([H|T], Acc) -> reverse_tail(T, [H|Acc]).

sublist(_, 0) -> [];
sublist([H|_], 1) -> [H];
sublist([H|T], N) when N > 1 -> [H] ++ sublist(T, N-1).

sublist_tail([], _) -> [];
sublist_tail(L, N) -> sublist_tail(L, N, []).
sublist_tail(_, 0, Acc) -> reverse_tail(Acc);
sublist_tail([H|T], N, Acc) when N > 0 -> sublist_tail(T, N-1, [H|Acc]).

zip([], []) -> [];
zip([H1|T1], [H2|T2]) -> [{H1, H2}] ++ zip(T1, T2).

lenient_zip([], _) -> [];
lenient_zip(_, []) -> [];
lenient_zip([H1|T1], [H2|T2]) -> [{H1, H2}|lenient_zip(T1, T2)].

zip_tail(L1, L2) -> zip_tail(L1, L2, []).
zip_tail(_, [], Acc) -> reverse_tail(Acc);
zip_tail([], _, Acc) -> reverse_tail(Acc);
zip_tail([H1|T1], [H2|T2], Acc) -> zip_tail(T1, T2, [{H1, H2}|Acc]).

%quicksort([]) -> [];
%quicksort(L) -> quicksort(L, [], [], []).
%quicksort([H|T]) -> quicksort() ++ [] ++ quicksort();

quicksort([]) -> [];
quicksort([Pivot|T]) ->
  {G, E, L} = partition(Pivot, T, [], [], []),
  quicksort(G) ++ E ++ quicksort(L).

partition(_, [], G, E, L) -> {G, E, L};
partition(Pivot, [H|T], G, E, L) ->
  case H of
    H when H > Pivot -> partition(Pivot, T, [H|G], E, L);
    H when H < Pivot -> partition(Pivot, T, G, E, [H|L]);
    H when H =:= Pivot -> partition(Pivot, T, G, [H|E], L);
    _ -> []
  end.

-ifdef(comment).
partition(_, [], G, L) -> {G, L};
partition(Pivot, [H|T], G, L) ->
  case H of
    H when H > Pivot -> partition(Pivot, T, [H|G], L);
    H when H =< Pivot -> partition(Pivot, T, G, [H|L]);
    _ -> []
  end.
-endif.



%quicksort(Pivot, [H|T]) ->
%  case H of
%    H when H >= Pivot -> [quicksort(Pivot, T)|H];
%    H when H < Pivot -> [H|quicksort(Pivot, T)];
%    _ ->
