#include <iostream>
#include <vector>

using namespace std;

void print_matrix(vector<vector<int>> m)
{
  for(int i = 0; i < m.size(); i++)
  {
    for(int j = 0; j < m[0].size(); j++)
    {
      cout << m[i][j] << " ";
    }
    cout << endl;
  }
  cout << endl;
}

int main(int argc, char const *argv[]) {
  int n = 5;
  vector<vector<int>> m1
  {{1,2,3,4,5},
    {6,7,8,9,10},
    {11,12,13,14,15},
    {16,17,18,19,20},
    {20,21,22,23,24}};
  vector<vector<int>> m2
    {{1,4,3,4,1},
      {6,7,3,9,11},
      {11,1,13,4,1},
      {1,7,18,9,0},
      {0,2,2,23,4}};
  vector<vector<int>> result(n,vector<int>(n,0));

  for(int i = 0; i < n; i++)
  {
    for(int j = 0; j < n; j++)
    {
      for(int k = 0; k < n; k++)
      {
        result[i][j] += m1[i][k] * m2[k][j];
      }
    }
  }
  print_matrix(result);
  return 0;
}
