defmodule Reset do
  defstruct [_values: %{}]

  def new(values) when is_map(values) do
    %Reset{_values: values}
  end

  def new(values) when is_list(values) do
    new_map = map_from_list(values, %{})
    %Reset{_values: new_map}
  end

  def items(reset) do
    Map.keys(reset._values)
  end

  def contains(reset, item) do
    case Map.fetch(reset._values, item) do
      {:ok, _} -> true
      _ -> false
    end
  end

  def intersect(reset, reset2) do
    old_items = items(reset)
    new_items = Enum.filter(old_items, fn(n) -> contains(reset2, n) end)
    new(new_items)
  end

  def union(reset, reset2) do
    items1 = items(reset)
    items2 = items(reset2)
    items3 = items1 ++ items2

    new_items = map_from_list(items3, %{})
    new(new_items)
  end

  def difference(reset, reset2) do
    u = union(reset, reset2)
    i = intersect(reset, reset2)
    u_items = items(u)

    new_items = Enum.filter(
      u_items,
      fn(u_item) -> (not contains(i, u_item)) end
    )

    new(new_items)
  end

  def subtract(reset, reset2) do
    i = intersect(reset, reset2)
    r_items = items(reset)

    new_items = Enum.filter(
      r_items,
      fn(r_item) -> (not contains(i, r_item)) end
    )

    new(new_items)
  end

  def map_from_list([head | tail], map) do
    map_from_list(tail, Map.put(map, head, head))
  end

  def map_from_list([], map) do
    map
  end

end
