#include <iostream>
#include <vector>
#include <chrono>


#include "ThreadPool.h"


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

int main()
{
    int n = 2;
    int threads = n;
    ThreadPool pool(threads);
    vector< future<int> > results;
    vector<vector<int>> m1,m2;
    m1 = gen_matrix(n);
    m2 = gen_matrix(n);
    print_matrix(m1);
    print_matrix(m2);
    auto start = chrono::system_clock::now();
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
    auto end = chrono::system_clock::now();

    chrono::duration<float,std::milli> duration = end - start;
    print_matrix(resultante);
    cout << "Time: " << duration.count() << " s" << endl;

    return 0;
}
