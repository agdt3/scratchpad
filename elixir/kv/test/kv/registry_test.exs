defmodule KV.RegistryTest do
  use ExUnit.Case, async: true

  setup context do
    {:ok, _} = start_supervised({KV.Registry, name: context.test})
    %{registry: context.test}
  end

  test "lookup on non-existing bucket throws error", %{registry: registry} do
    assert KV.Registry.lookup(registry, "grocery_list") == :error
  end

  test "create spawns new buckets", %{registry: registry} do
    KV.Registry.create(registry, "grocery_list")
    assert {:ok, bucket} = KV.Registry.lookup(registry, "grocery_list")
    KV.Bucket.put(bucket, "milk", 1)
    assert KV.Bucket.get(bucket, "milk") == 1
  end

  test "removes buckets on exit", %{registry: registry} do
    KV.Registry.create(registry, "grocery_list")
    {:ok, bucket} = KV.Registry.lookup(registry, "grocery_list")

    Agent.stop(bucket, :normal)
    # Makes sure that the async :DOWN info message is processed by the registry
    _ = KV.Registry.create(registry, "bogus")
    assert KV.Registry.lookup(registry, "grocery_list") == :error
  end

  test "removes bucket on crash", %{registry: registry} do
    KV.Registry.create(registry, "grocery_list")
    {:ok, bucket} = KV.Registry.lookup(registry, "grocery_list")

    # Shutdown replicates a bucket crashing
    # Should not crash the registry too!
    Agent.stop(bucket, :shutdown)
    assert KV.Registry.lookup(registry, "grocery_list") == :error
  end
end
