require Logger

defmodule KVServer do
  @moduledoc """
  Documentation for KVServer.
  """

  def accept(port) do
    # listen to port until socket becomes available
    # {:ok, socket} = :gen_tcp.listen(port, [:binary, packet: :line, active: false, reuseaddr: false])

    case :gen_tcp.listen(port, [:binary, packet: :line, active: false, reuseaddr: false]) do
      {:ok, socket} -> {
        Logger.info("Accepting connections on port #{port}")
        loop_acceptor(socket)
      }
      {:err, reason} -> raise err
    end
    #Logger.info("Accepting connections on port #{port}")

    #loop_acceptor(socket)
  end

  # accepts connections on socket
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

  defp read_line(socket) do
    :gen_tcp.recv(socket, 0)
  end

  defp write_line(socket, {:ok, text}) do
    :gen_tcp.send(socket, text)
  end

  defp write_line(socket, {:error, :unknown_command}) do
    # Unknown Command
    :gen_tcp.send(socket, "UNKNOWN COMMAND\r\n")
  end

  defp write_line(socket, {:error, :key_not_found, key}) do
    # Key not found
    :gen_tcp.send(socket, "KEY #{key} NOT FOUND\r\n")
  end

  defp write_line(socket, {:error, :bucket_not_found}) do
    # Bucket not found
    :gen_tcp.send(socket, "BUCKET NOT FOUND\r\n")
  end

  defp write_line(_socket, {:error, :closed}) do
    # The connection was closed, exit politely.
    exit(:shutdown)
  end

  defp write_line(socket, {:error, error}) do
    # Unknown error. Write to the client and exit.
    :gen_tcp.send(socket, "ERROR\r\n")
    exit(error)
  end

 end
