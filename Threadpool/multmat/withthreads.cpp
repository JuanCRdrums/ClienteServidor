#include <iostream>
#include <vector>
#include <chrono>

#include "ThreadPool.h"


using namespace std;


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
    int r;
    for(int i = 0; i < threads; ++i) {
        results.emplace_back(
            pool.enqueue([i] {
                cout << "hello " << i << endl;
                this_thread::sleep_for(chrono::seconds(1));
                cout << "world " << i << endl;
                return i*i;
            })
        );
    }

    for(auto && result: results)
        cout << result.get() << ' ';
    cout << endl;

    return 0;
}
