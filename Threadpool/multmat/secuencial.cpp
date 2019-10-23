#include <iostream>
#include <vector>
#include <chrono>

using namespace std;

vector<vector<int>> gen_matrix( int n)
{
  vector<vector<int>> m;
  for(int i = 0; i < n; i++)
  {
    vector<int> aux;
    for(int j = 0; j < n; j++)
    {
      aux.push_back(rand() % 100);
    }
    m.push_back(aux);
  }
  return m;
}


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
  int n = 2;
  vector<vector<int>> m1,m2;
  m1 = gen_matrix(n);
  m2 = gen_matrix(n);
  print_matrix(m1);
  print_matrix(m2);
  vector<vector<int>> result(n,vector<int>(n,0));
  auto start = chrono::system_clock::now();

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
  auto end = chrono::system_clock::now();

  chrono::duration<float,std::milli> duration = end - start;

  print_matrix(result);
  cout << "Time: " << duration.count() << " s" << endl;
  return 0;
}
