defmodule KVServer.CommandTest do
  use ExUnit.Case, async: true
  doctest KVServer.Command

  setup context do
    {:ok, _} = start_supervised({KV.Registry, name: context.test})
    %{registry: context.test}
  end

  test "create bucket in registry", %{registry: registry} do
    assert KVServer.Command.run({:create, "testing"}, registry) == {:ok, "OK\r\n"}
  end

  test "put value at key in bucket in registry", %{registry: registry} do
    KVServer.Command.run({:create, "testing"}, registry)
    assert KVServer.Command.run({:put, "testing", "milk", 3}, registry) == {:ok, "OK\r\n"}
  end

  test "get value from bucket in registry", %{registry: registry} do
    KVServer.Command.run({:create, "testing"}, registry)
    KVServer.Command.run({:put, "testing", "milk", 3}, registry)
    assert KVServer.Command.run({:get, "testing", "milk"}, registry) == {:ok, "3\r\nOK\r\n"}
  end

  test "get value from empty bucket in registry", %{registry: registry} do
    KVServer.Command.run({:create, "testing"}, registry)
    assert KVServer.Command.run({:get, "testing", "milk"}, registry) == {:error, :key_not_found, "milk"}
  end

  test "get value from non-existent bucket in registry", %{registry: registry} do
    assert KVServer.Command.run({:get, "testing", "milk"}, registry) == {:error, :bucket_not_found}
  end

  test "delete value from bucket in registry", %{registry: registry} do
    KVServer.Command.run({:create, "testing"}, registry)
    KVServer.Command.run({:put, "testing", "milk", 3}, registry)
    assert KVServer.Command.run({:delete, "testing", "milk"}, registry) == {:ok, "OK\r\n"}
  end
end

