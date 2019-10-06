defmodule KV.Registry do
  use GenServer

  ## Client API

  @doc """
  Start the registry
  """
  def start_link(opts) do
    server = Keyword.fetch!(opts, :name)
    GenServer.start_link(__MODULE__, server, opts)
  end

  @doc """
  Looks up the bucket pid for `name` stored in `server`.
  Returns `{:ok, pid}` if the bucket exists, `:error` otherwise.
  """
  def lookup(server, name) do
    #GenServer.call(server, {:lookup, name})
    case :ets.lookup(server, name) do
      [{^name, pid}] -> {:ok, pid}
      [] -> :error
    end
  end

  @doc """
  Ensures there is a bucket associated with the given `name` in `server`.
  """
  def create(server, name) do
    #GenServer.cast(server, {:create, name})
    GenServer.call(server, {:create, name})
  end

  def stop(server) do
    GenServer.stop(server)
  end

  ## Server callbacks

  def init(table) do
    #names = %{}
    names = :ets.new(table, [:named_table, read_concurrency: true])
    refs = %{}
    {:ok, {names, refs}}
  end

  #def handle_call({:lookup, name}, _from, {names, _} = state) do
  #  {:reply, Map.fetch(names, name), state}
  #end

  def handle_call({:create, name}, _from, {names, refs}) do
    case lookup(names, name) do
      {:ok, pid} ->
        {:reply, pid, {names, refs}}
      :error ->
        {:ok, pid} = KV.BucketSupervisor.start_bucket()
        ref = Process.monitor(pid)
        refs = Map.put(refs, ref, name)
        :ets.insert(names, {name, pid})
        {:reply, pid, {names, refs}}
    end
  end

  #def handle_cast({:create, name}, {names, refs}) do
    #if Map.has_key?(names, name) do
    #  {:reply, {names, refs}}
    #else
    #  {:ok, pid} = KV.BucketSupervisor.start_bucket()
    #  ref = Process.monitor(pid)
    #  refs = Map.put(refs, ref, name)
    #   names = Map.put(names, name, pid)
    #  {:reply, {names, refs}}
    #end
  #end

  def handle_info({:DOWN, ref, :process, _pid, _reason}, {names, refs}) do
    {name, refs} = Map.pop(refs, ref)
    #names = Map.delete(names, name)
    :ets.delete(names, name)
    {:noreply, {names, refs}}
  end

  def handle_info(_msg, state) do
    {:noreply, state}
  end
end
