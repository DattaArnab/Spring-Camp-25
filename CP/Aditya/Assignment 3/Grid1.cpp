#include <bits/stdc++.h>
using namespace std;
#define rep(i, a, b) for(int i = a; i < b; ++i)
#define tr(a, x) for(auto& a : x)
#define all(x) x.begin(), x.end()
#define sz(x) (int)(x).size()
#define w(a) while(a--)
#define cint(n) int n; cin >> n;
#define endl '\n'
typedef long long ll;
typedef long double ld;
typedef pair<int, int> pi;
typedef vector<int> vi;
typedef vector<string> vs;
#define MOD 1000000007;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    int h, w;
    cin >> h >> w;
    vector<vector<char>> grid(h, vector<char>(w));
    vector<vi> dp(h, vi(w, 0));
    rep(i, 0, h) {
        rep(j, 0, w) {
            cin >> grid[i][j];
        }
    }
    dp[0][0] = (grid[0][0] == '.' ? 1 : 0);
    rep(i, 0, h) {
        rep(j, 0, w) {
            if (grid[i][j] == '#') continue;
            if (i > 0) dp[i][j] = (dp[i][j] + dp[i-1][j])%MOD;
            if (j > 0) dp[i][j] = (dp[i][j] + dp[i][j-1])%MOD;  
        }
    }
    cout << dp[h-1][w-1] << endl;
}
