defmodule KV do
  use Application

  @moduledoc """
  Documentation for KV.
  Application callback module
  """

  def start(_type, _args) do
    KV.Supervisor.start_link(name: KV.Supervisor)
  end

end
