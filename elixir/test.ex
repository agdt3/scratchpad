defmodule A do
  def sa() do
    IO.inspect sortarray([5, 1, 7, 4, 6, 5, 3], [], [], [])
  end

  def sortarray([], less, mid, more) do
    [less: less, mid: mid, more: more]
  end

  def sortarray([head], less, mid, more) do
    sortarray([], less, [head | mid], more)
  end

  def sortarray([head | [head2 | tail]], less, mid, more) do
    case {head, head2} do
      {head, head2} when head2 > head -> sortarray([head | tail], less, mid, [head2 | more])
      {head, head2} when head2 == head -> sortarray([head | tail], less, [head2 | mid], more)
      {head, head2} when head2 < head -> sortarray([head | tail], [head2 | less], mid, more)
    end
  end
end

defmodule Test do
  def fib(1) do
    0
  end

  def fib(2) do
    1
  end

  def fib(n) when n < 1 do
    "Error"
  end

  def fib(n) when n > 2 do
    fib(n-1) + fib(n-2)
  end
end

defmodule Test2 do
  def fib(index) do
    if (index < 3) do
      _fib(0, 1, index-1)
    else
      _fib(0, 1, index-2)
    end
  end

  def _fib(v1, v2, 0) do
    0
  end

  def _fib(v1, v2, 1) do
    v1 + v2
  end

  def _fib(v1, v2, index) do
    _fib(v2, v1 + v2, index-1)
  end
end

defmodule Qsort do
  def srt() do
    start_list = [4, 15, 8, 3, 2, 4, 8, 1, 9]
    end_list = [1, 2, 3, 4, 4, 8, 8, 9, 15]
    result = qsort(start_list)
    IO.inspect result
    if end_list !== result do
      "Result is busted"
    else
      "Worked!"
    end
  end

  defp qsort([]) do
   []
  end

  defp qsort([head]) do
    [head]
  end

  defp qsort([head | tail]) do
    {less, mid, more} = sortarray([head | tail], [], [], [])
    qsort(less) ++ mid ++ qsort(more)
  end

  defp sortarray([], less, mid, more) do
    {less, mid, more}
  end

  defp sortarray([head], less, mid, more) do
    sortarray([], less, [head | mid], more)
  end

  defp sortarray([head | [head2 | tail]], less, mid, more) do
    case {head, head2} do
      {head, head2} when head2 > head -> sortarray([head | tail], less, mid, [head2 | more])
      {head, head2} when head2 == head -> sortarray([head | tail], less, [head2 | mid], more)
      {head, head2} when head2 < head -> sortarray([head | tail], [head2 | less], mid, more)
    end
  end

end
