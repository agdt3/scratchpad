#include <iostream>
#include <stack>
#include <string>

struct Bracket {
    Bracket(char type, int position):
        type(type),
        position(position)
    {}

    bool Matchc(char c) {
        if (type == '[' && c == ']')
            return true;
        if (type == '{' && c == '}')
            return true;
        if (type == '(' && c == ')')
            return true;
        return false;
    }

    char type;
    int position;
};

int main() {
    std::string text;
    getline(std::cin, text);
    int failed_position = -1;

    std::stack <Bracket> opening_brackets_stack;
    for (int position = 0; position < text.length(); ++position) {
        char next = text[position];

        if (next == '(' || next == '[' || next == '{') {
            Bracket bracket = Bracket(next, position);
            opening_brackets_stack.push(bracket);
        }

        if (next == ')' || next == ']' || next == '}') {
            if (opening_brackets_stack.size() > 0 &&
                opening_brackets_stack.top().Matchc(next)) {
              opening_brackets_stack.pop();
            }
            else {
              failed_position = position + 1;
              break;
            }
        }
    }

    if (opening_brackets_stack.size() > 0 || failed_position != -1) {
      std::cout << failed_position;
    }
    else {
      std::cout << "Success";
    }

    // Printing answer, write your code here

    return 0;
}
