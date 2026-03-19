// D - Snuke's Coloring 
// 3000ms, 256MB

#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
#define int ll
const int _=300005, _m=998244353; mt19937_64 rnd(98275314); int qpow(int a, int b) {int ret=1;while(b) {if(b&1) ret=ret*a%_m;b>>=1; a=a*a%_m;}return ret;}int inv(int a) {return qpow(a, _m-2);}int gcd(int a, int b) {return b==0?a:gcd(b, a%b);}int lcm(int a, int b) {return a/gcd(a, b)*b;}int dx[8]={1, -1, 0, 0, 1, -1, 1, -1}, dy[8]={0, 0, 1, -1, 1, 1, -1, -1};
int h, w, n, ans[_];
void solve() {
    cin>>h>>w>>n; map<pair<int, int>, int> m;
    for(int i=1; i<=n; i++) {
        int u, v; cin>>u>>v;
        for(int x=u-2; x<=u; x++) {
            for(int y=v-2; y<=v; y++) {
                if(x>=1&&y>=1&&x+2<=h&&y+2<=w) m[{x, y}]++;
            }
        }
    }
    ans[0]=(h-2)*(w-2);
    for(auto &[p, cnt]: m) {
        ans[cnt]++; ans[0]--;
    }
    for(int i=0; i<=9; i++) cout<<ans[i]<<'\n';
} //yunayu_2026_target_M

signed main() {
    cin.tie(0)->sync_with_stdio(0);
    solve();
    // int T; cin>>T; while(T--) solve();
    return 0;
} //"日拱一卒，功不唐捐。"