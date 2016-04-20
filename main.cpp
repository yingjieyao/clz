// Copyright (c) 2015 , yogurt.yyj.
// All rights reserved.
//
// Filename:  main.cpp
//
// Description: Main file
//
// Version:  1.0
// Created:  2016/04/18 18时39分59秒
// Compiler:  g++
//
// Author:  yogurt (yyj), yyjhit@sina.com
//

#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
#include <fstream>

using namespace std;

#define mp make_pair
#define pb push_back
#define ll long long

// #define GENERATE_RAND

// 总共的人数
const static int PERSON = 8;
// 每个人的需求数
const static int PER_REQUEST = 4;
// 每个人满意度的和
const static int SUM_SATISFY = 100;
// 每个需求最大的耗费资源数
const static int MAX_CONSUME = 1000;
//
const static int A = 3;
const static int B = 1;
const static int C = 1;

template<typename T>
void print(const vector<T> &in) {
    int n = in.size();
    for (int i = 0; i < n; ++i) {
        cout << in[i] << ' ';
    }
    cout << endl;
}


// 生成随机数矩阵，存到文件rand.txt中
bool generate_rand() {

    ofstream out("rand.txt");

    if (!out.is_open()) return false;

    srand(time(NULL));

    for (int per = 1; per <= PERSON; ++per) {
        vector<pair<int, int> > ev;
        ev.clear();
        int cur_sum = 0;
        for (int req = 1; req <= PER_REQUEST; ++req) {
            int satisfy = rand() % SUM_SATISFY + 1; //
            int consume = rand() % MAX_CONSUME + 1; // 1 - MAX_CONSUME
            cur_sum += satisfy;
            ev.pb(mp(satisfy, consume));
        }

        int left = SUM_SATISFY;
        for (int req = 1; req <= PER_REQUEST; ++req) {
            int satisfy = int(ev[req - 1].first * 100.0 / cur_sum + 0.5);
            if (req == PER_REQUEST) {
                satisfy = left;
            }
            out << satisfy << '\t' << ev[req - 1].second << endl;
            left -= satisfy;
        }
    }

    out.close();
    return true;
}

// 从rand.txt中读取数据
vector<pair<int, int> > read_data() {
    vector<pair<int, int> > ans;
    ans.clear();
    ifstream in("rand.txt");
    if (!in.is_open()) return ans;
    int satisfy, consume;
    while (in >> satisfy >> consume) {
        ans.pb(mp(satisfy, consume));
    }
    return ans;
}

// 计算方差
double variance(const vector<int> &in) {
    double sum = 0, sum2 = 0;
    int n = in.size();

    if (!n) return 0;

    for (int i = 0; i < n; ++i) {
        sum += in[i];
        sum2 += in[i] * in[i];
    }
    sum /= n, sum2 /= n;
    // D(x) = E(x^2) - E(x)^2
    return sum2 - sum * sum;
}

double sum(const vector<int> &in) {
    double sum = 0;
    int n = in.size();
    for (int i = 0; i < n; ++i) {
        sum += in[i];
    }
    return sum;
}

double average(const vector<int> &in) {
    if (in.size() == 0) return 0;
    return sum(in) / in.size();
}

double calc_P(const vector<int> &satisfy, const vector<int> &consume) {
    // cout << satisfy.size() << consume.size() << endl;

    // cout << "satisfy "; print(satisfy);
    // cout << "consume "; print(consume);
    // cout << "average " << average(satisfy) << ' ' << variance(satisfy) << endl;
    return A * average(satisfy) / 100.0 - B / 0.25 * variance(satisfy) -
         C * average(consume);
}

int main() {

#ifdef GENERATE_RAND
    if (!generate_rand()) {
        cout << "Generate rand matrix failed" << endl;
        return 0;
    }
#endif

    vector<pair<int, int> > data = read_data();
    // for (size_t i = 0; i < data.size(); ++i) {
    //     cout << data[i].first << '\t' << data[i].second << endl;
    // }

    ll max_iter = 1LL << (PERSON * PER_REQUEST);
    vector<double> ans;
    ans.clear();
    for (ll i = 0; i < max_iter; ++i) {
        vector<int> satisfy, consume;  // 每个人的满意度以及消耗的资源
        satisfy.clear(), consume.clear();
        for (int index = 0; index  < PERSON; ++index) {
            satisfy.pb(0), consume.pb(0);
        }
        for (int index = 0; index < (PERSON * PER_REQUEST); ++index) {
            if ((i >> index) & 1) {
                satisfy[index / 4] += data[index].first;
                consume[index / 4] += data[index].second;
            }
        }
        // cout << i << '\t'  << calc_P(satisfy, consume) << endl;
        ans.pb(calc_P(satisfy, consume));
    }


    int ans_pos = -1;
    double ans_max = INT_MIN * 1.0;
    for (ll i = 0; i < max_iter; ++i) {
        if (ans[i] > ans_max) {
            ans_max = ans[i];
            ans_pos = i;
        }
    }
    cout << ans_pos << ' ' << ans_max << endl;

    return 0;
}
