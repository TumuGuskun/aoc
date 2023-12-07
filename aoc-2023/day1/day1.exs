contents = File.read!("input.txt")

defmodule Line do
  def parse_numeric(line) do
    line = String.replace(line, ~r/[a-z\n]/, "")
    String.to_integer(String.at(line, 0) <> String.at(line, -1))
  end

  def parse_alphanumeric(line) do
    string_integers = []

    Enum.with_index(line, fn char, index ->
      if String.contains?(char, ~r/[0-9]/) do
        string_integers = [char]
      else
        if char == String.at(line, index - 1) do
          string_integers = string_integers ++ [char]
        end
      end
    end)

    line = String.replace(line, ~r//, "")
    String.to_integer(String.at(line, 0) <> String.at(line, -1))
  end
end

IO.puts("part 1")

IO.puts(
  contents
  |> String.split("\n")
  |> Enum.map(fn line -> Line.parse_numeric(line) end)
  |> Enum.reduce(0, fn number, acc -> number + acc end)
)

IO.puts("part 2")

IO.puts(
  contents
  |> String.split("\n")
  |> Enum.map(fn line -> Line.parse_alphanumeric(line) end)
  |> Enum.reduce(0, fn number, acc -> number + acc end)
)
