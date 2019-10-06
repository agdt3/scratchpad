defmodule KV.RouterTest do
  use ExUnit.Case, async: true

  @tag :distributed
  test "route requests across nodes" do
    assert KV.Router.route("hello", Kernel, :node, []) == :"foo@L01605"
    assert KV.Router.route("world", Kernel, :node, []) == :"bar@L01605"
  end

  test "raise on unknown entries" do
    assert_raise(RuntimeError, ~r/Could not find entry/, fn -> KV.Router.route(<<0>>, Kernel, :node, []) end)
  end
end