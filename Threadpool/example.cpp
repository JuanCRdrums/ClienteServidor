#include <iostream>
#include <vector>
#include <chrono>

#include "ThreadPool.h"


using namespace std;


int main()
{
    int n = thread::hardware_concurrency();
    ThreadPool pool(n);
    vector< future<int> > results;

    for(int i = 0; i < n; ++i) {
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
