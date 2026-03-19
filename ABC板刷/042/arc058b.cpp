// D - Iroha and a Grid 
// 2000ms, 256MB

#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
#define int ll
const int _=300005, _m=1e9+7; mt19937_64 rnd(98275314); int qpow(int a, int b) {int ret=1;while(b) {if(b&1) ret=ret*a%_m;b>>=1; a=a*a%_m;}return ret;}int inv(int a) {return qpow(a, _m-2);}int gcd(int a, int b) {return b==0?a:gcd(b, a%b);}int lcm(int a, int b) {return a/gcd(a, b)*b;}int dx[4]={1, -1, 0, 0}, dy[4]={0, 0, 1, -1};
int h, w, a, b, nx[_];
int C(int a, int b) {
    if(a<b) return 0;
    return nx[a]*inv(nx[b])%_m*inv(nx[a-b])%_m;
}
void solve() {
    cin>>h>>w>>a>>b;
    int yu=h-a+b+1, __=0;
    for(int i=b+1; i<=w; i++) {
        int x=yu-i, y=i; if(!x) break;
        __=(__+C(x-1+y-1, x-1)*C(h-x+w-y, h-x))%_m;
    }
    cout<<__<<'\n';
} //yunayu_2026_target_M

signed main() {
    cin.tie(0)->sync_with_stdio(0);
    nx[0]=1;
    for(int i=1; i<=200005; i++) {
        nx[i]=nx[i-1]*i%_m;
    }
    solve();
    // int T; cin>>T; while(T--) solve();
    return 0;
} //"日拱一卒，功不唐捐。"