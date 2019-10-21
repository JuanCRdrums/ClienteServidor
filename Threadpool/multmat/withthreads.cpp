#include <iostream>
#include <vector>
#include <chrono>

#include "ThreadPool.h"


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

int main()
{
    int n = 5;
    int threads = n*n;
    ThreadPool pool(threads);
    vector< future<int> > results;
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

    vector<vector<int>> resultante(n);
    for(int i = 0; i < n; ++i) {
      for(int j = 0; j < n; j++)
      {
        results.emplace_back(
            pool.enqueue([m1,m2,i,j,n] {
                /*cout << "hello " << m1[i] << endl;
                this_thread::sleep_for(chrono::seconds(1));
                cout << "world " << m1[i] << endl;*/
                //cout << m1[i][j] << endl;
                int r = 0;
                for(int k = 0; k < n; k++)
                {
                  r += m1[i][k] * m2[k][j];
                }
                return r;
            })
        );
      }
    }
    int i = 0,cont = 0;
    for(auto && result: results)
    {
      if(cont == n)
      {
          i++;
          cont = 0;
      }
      int num = result.get();
      resultante[i].push_back(num);
      cont++;
    }
    print_matrix(resultante);


    return 0;
}
