defmodule KV.Supervisor do
  use Supervisor

  def start_link(opts) do
    Supervisor.start_link(__MODULE__, :ok, opts)
  end

  def init(:ok) do
    children = [
      KV.BucketSupervisor,
      {KV.Registry, name: KV.Registry}
    ]
    # one_for_all restarts all children if one crashes
    # in this case if registry crashes, we restart bucket_supervisor and vice versa
    Supervisor.init(children, strategy: :one_for_all)
  end
end
