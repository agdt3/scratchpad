-module(functions).
-compile(export_all).

head([X | _]) ->
  X.

second([_, X | _]) ->
  X.

test() ->
  io:format("~s~n",[<<"Hello">>]),
  io:format("~p~n",[<<"Hello">>]),
  io:format("~~~n"),
  io:format("~f~n", [4.0]),
  io:format("~30f~n", [4.0]).

range_and(X) when X >= 10, X =< 100 ->
  true;
range_and(_) ->
  false.

range_or(X) when X =< 10; X >= 100 ->
  true;
range_or(_) ->
  false.
