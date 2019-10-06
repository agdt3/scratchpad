defmodule KVServer.Command do
  @doc ~S"""
  Parses the given line into a command

  ## Examples
    iex> KVServer.Command.parse "CREATE  shopping\r\n"
    {:ok, {:create, "shopping"}}

    iex> KVServer.Command.parse "CREATE  shopping \r\n"
    {:ok, {:create, "shopping"}}

    iex> KVServer.Command.parse "PUT shopping milk 1\r\n"
    {:ok, {:put, "shopping", "milk", "1"}}

    iex> KVServer.Command.parse "GET shopping milk\r\n"
    {:ok, {:get, "shopping", "milk"}}

    iex> KVServer.Command.parse "DELETE shopping eggs\r\n"
    {:ok, {:delete, "shopping", "eggs"}}

    Unknown commands or commands with the wrong number of
    arguments return an error:

    iex> KVServer.Command.parse "UNKNOWN shopping eggs\r\n"
    {:error, :unknown_command}

    iex> KVServer.Command.parse "GET shopping\r\n"
    {:error, :unknown_command}
  """

  def parse(line) do
    case String.split(line) do
      ["CREATE", bucket] -> {:ok, {:create, bucket}}
      ["GET", bucket, key] -> {:ok, {:get, bucket, key}}
      ["PUT", bucket, key, value] -> {:ok, {:put, bucket, key, value}}
      ["DELETE", bucket, key] -> {:ok, {:delete, bucket, key}}
      _ -> {:error, :unknown_command}
    end
  end

  def run({:create, bucket}, registry_pid) do
    KV.Registry.create(registry_pid, bucket)
    {:ok, "OK\r\n"}
  end

  def run({:get, bucket, key}, registry_pid) do
    lookup(bucket, registry_pid, fn bucket_pid ->
      case KV.Bucket.get(bucket_pid, key) do
        nil -> {:error, :key_not_found, key}
        value -> {:ok, "#{value}\r\nOK\r\n"}
      end
    end)
  end

  def run({:put, bucket, key, value}, registry_pid) do
    lookup(bucket, registry_pid, fn bucket_pid ->
      KV.Bucket.put(bucket_pid, key, value)
      {:ok, "OK\r\n"}
    end)
  end

  def run({:delete, bucket, key}, registry_pid) do
    lookup(bucket, registry_pid, fn bucket_pid ->
      KV.Bucket.delete(bucket_pid, key)
      {:ok, "OK\r\n"}
    end)
  end

  defp lookup(bucket, registry_pid, callback) do
    case KV.Registry.lookup(registry_pid, bucket) do
      {:ok, pid} -> callback.(pid)
      :error -> {:error, :bucket_not_found}
    end
  end
end
