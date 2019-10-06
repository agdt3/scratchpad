-module(exc).
-compile(export_all).

throws(F) ->
  try F() of
    _ -> ok
  catch
    Throw -> {throw, caught, Throw}
  end.

errors(F) ->
  try F() of
    _ -> ok
  catch
    error:Error -> {throw, caught, Error}
  end.

exits(F) ->
  try F() of
    _ -> ok
  catch
    exit:Exit -> {throw, caught, Exit}
  end.


black_knight(Attack) when is_function(Attack, 0) ->
  try Attack() of
    _ -> "None shall pass"
  catch
    throw:slice -> "But a scratch";
    error:cut_arm -> "I've had worse";
    exit:cut_leg -> "I'm still standing";
    _:_ -> "But a flesh wound"
  after
    "falls over"
  end.
