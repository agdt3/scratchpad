#include <iostream>
#include <vector>

//#define l[]() []()

int main() {
  std::vector<int> a {1, 2, 3, 4};
  for_each(a.begin(), a.end(), [] (int x){
    std::cout << x << std::endl;
  });

  return EXIT_SUCCESS;
}
