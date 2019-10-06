require Logger

defmodule Sockets.Server do
  def accept(port) do
    # listen to port until socket becomes available
    {:ok, socket} = :gen_tcp.listen(port, [:binary, packet: :line, active: false, reuseaddr: false])
    Logger.info("Accepting connections on port #{port}")

    loop_acceptor(socket)
  end

  defp loop_acceptor(socket) do
    {:ok, client} = :gen_tcp.accept(socket)

    # Create a new child task to serve client connection
    {:ok, pid} = Task.Supervisor.start_child(KVServer.TaskSupervisor, fn -> serve(client) end)

    # child process becomes controlling process of client conn
    # so that a crashing client won't bring down this process
    :ok = :gen_tcp.controlling_process(client, pid)

    loop_acceptor(socket)
  end

  defp serve(socket) do
    msg =
      with {:ok, data} <- read_line(socket),
           {:ok, command} <- KVServer.Command.parse(data)
      do KVServer.Command.run(command, KV.Registry) end

    write_line(socket, msg)
    serve(socket)
  end
end
