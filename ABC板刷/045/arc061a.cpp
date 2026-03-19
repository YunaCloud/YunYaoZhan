// C - Many Formulas 
// 2000ms, 256MB

#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
#define int ll
const int _=300005, _m=998244353; mt19937_64 rnd(98275314); int qpow(int a, int b) {int ret=1;while(b) {if(b&1) ret=ret*a%_m;b>>=1; a=a*a%_m;}return ret;}int inv(int a) {return qpow(a, _m-2);}int gcd(int a, int b) {return b==0?a:gcd(b, a%b);}int lcm(int a, int b) {return a/gcd(a, b)*b;}int dx[4]={1, -1, 0, 0}, dy[4]={0, 0, 1, -1};
int n; string s; vector<int> a;
void dfs(int x, string y) {
    if(x==n) {
        int sum=0, t=0; y+='1';
        for(int i=0; i<n; i++) {
            t=10*t+s[i]-'0';
            if(y[i]=='1') {
                sum+=t; t=0;
            }
        }
        a.push_back(sum); return;
    }
    dfs(x+1, y+'1');
    dfs(x+1, y+'0');
}
void solve() {
    cin>>s; n=s.size();
    dfs(1, "");
    int __=0;
    for(auto &ele: a) __+=ele;
    cout<<__<<'\n'; 
} //yunayu_2026_target_M

signed main() {
    cin.tie(0)->sync_with_stdio(0);
    solve();
    // int T; cin>>T; while(T--) solve();
    return 0;
} //"日拱一卒，功不唐捐。"