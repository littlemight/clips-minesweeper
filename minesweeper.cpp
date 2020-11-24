#include <bits/stdc++.h>


#define fi first
#define se second
#define pb(a) push_back(a)
#define mp(a, b) make_pair(a, b)
#define el '\n'

using namespace std;
using ll = long long;
using pii = pair<int, int>;

mt19937 rng32(chrono::steady_clock::now().time_since_epoch().count());
const int MINN = 4, MAXN = 10;

int n, bombCnt;
int isiCnt = 0;
vector<vector<bool>> bomb;
vector<vector<int>> mat;
vector<vector<int>> board;

int di[8] = {-1, -1, -1, 0, 0, 1, 1, 1};
int dj[8] = {-1, 0, 1, -1, 1, -1, 0, 1};

void print_board(){
    cout << "=======================" << el;
    for (int i=1;i<=n;i++){
        for (int j=1;j<=n;j++){
            cout << board[i][j] << " ";
        }
        cout << el;
    }
    cout << "=======================" << el;
}
bool comp_candidate(const pair<pii, pii>& a, const pair<pii, pii>& b){
    if (a.fi == mp(0, 0)) return 0;
    if (b.fi == mp(0, 0)) return 1;
    pii ra = a.fi;
    pii rb = b.fi;
    if (ra.fi < ra.se) swap(ra.fi, ra.se);
    if (rb.fi < rb.se) swap(rb.fi, rb.se);
    return 1LL * ra.fi * rb.se > 1LL * rb.fi * ra.se;
}
void kalah(){
    cout << "KAU KALAH!!" << el;
    exit(0);
}

void init(){
    for (int i=1;i<=n;i++){
        for (int j=1;j<=n;j++){
            if (bomb[i][j]){
                mat[i][j] = -1;
                continue;
            }
            for (int id=0;id<8;id++){
                int ni = i + di[id];
                int nj = j + dj[id];
                mat[i][j] += bomb[ni][nj];
            }
        }
    }
}
bool selesai(){
    for (int i=1;i<=n;i++){
        for (int j=1;j<=n;j++){
            if (board[i][j] == -2) return 0;
        }
    }
    return 1;
}
bool is_valid(const vector<vector<int>>& vec){
    for (int i=1;i<=n;i++){
        for (int j=1;j<=n;j++){
            if (vec[i][j] < 0 || vec[i][j] == 9) continue;
            int cur = 0;
            int kos = 0;
            for (int id=0;id<8;id++){
                int ni = i + di[id];
                int nj = j + dj[id];
                cur += vec[ni][nj] == -1;
                kos += vec[ni][nj] == -2;
            }
            if (cur > vec[i][j]) return 0;
            if (cur + kos < vec[i][j]) return 0;
        }
    }
    return 1;
}
bool in_range(int i, int j){
    return 1 <= i && i <= n && 1 <= j && j <= n;
}
void dfs(pii node){
    board[node.fi][node.se] = mat[node.fi][node.se];
    if (mat[node.fi][node.se] > 0) return;
    for (int i=0;i<8;i++){
        auto nnode = mp(node.fi + di[i], node.se + dj[i]);
        if (board[nnode.fi][nnode.se] != -2 || !in_range(nnode.fi, nnode.se)) continue;
        dfs(nnode);
    }
}
void make_assert(int i, int j, int val){
    if (val){
        if (mat[i][j] != -1){
            cout << "(" << i << ", " << j << ") bukan bomb" << el;
            kalah();
        }
    } else{
        if (mat[i][j] == -1){
            cout << "(" << i << ", " << j << ") adalah bomb" << el;
            kalah();
        }
    }
    if (!val){
        dfs(mp(i, j));
    } else{
        board[i][j] = mat[i][j];
    }
}
void makeOneMove(){
    vector<pair<pii, pii>> candidate;
    for (int i=1;i<=n;i++){
        for (int j=1;j<=n;j++){
            if (board[i][j] != -2){
                if (board[i][j] >= 0){
                    int udh = 0;
                    vector<pii> kosong;
                    for (int id=0;id<8;id++){
                        int ni = i + di[id];
                        int nj = j + dj[id];

                        if (!in_range(ni, nj)) continue;
                        if (board[ni][nj] == -2) kosong.pb(mp(ni, nj));
                        else if (board[ni][nj] == -1) udh++;
                    }
                    if (kosong.empty()) continue;
                    if (board[i][j] == udh){
                        for (auto x : kosong){
                            make_assert(x.fi, x.se, 0);
                        }
                        return;
                    } else if (board[i][j] == udh + (int)kosong.size()){
                        for (auto x : kosong){
                            make_assert(x.fi, x.se, 1);
                        }
                        return;
                    }
                }
                continue;
            }
            vector<pii> kosong;
            kosong.pb(mp(i, j));
            for (int id=0;id<8;id++){
                int ni = i + di[id];
                int nj = j + dj[id];

                if (!in_range(ni, nj)) continue;
                if (board[ni][nj] == -2) kosong.pb(mp(ni, nj));
            }

            pii chance = {0, 0};
            int len = kosong.size();
            for (int mask=0;mask<(1 << len);mask++){
                for (int id=0;id<len;id++){
                    auto pos = kosong[id];
                    if (mask & (1 << id)){
                        board[pos.fi][pos.se] = -1;
                    } else{
                        board[pos.fi][pos.se] = 9;
                    }
                }
                if (is_valid(board)){
                    if (mask & 1){
                        chance.se++;
                    } else{
                        chance.fi++;
                    }
                }
            }
            candidate.pb(mp(chance, mp(i, j)));
            for (auto x : kosong){
                board[x.fi][x.se] = -2;
            }
        }
    }
    if (candidate.empty()){
        print_board();
        kalah();
    }
    sort(candidate.begin(), candidate.end(), comp_candidate);
    int seri = 0;
    {
        pii pivot = candidate[0].fi;
        for (int i=1;i<(int)candidate.size();i++){
            pii cur = candidate[i].fi;
            if (pivot.fi * cur.se == pivot.se * cur.fi){
                seri++;
            } else{
                break;
            }
        }
    }
    auto pil_id = rng32() % (seri + 1);
    auto choosen = candidate[(int)pil_id];
    if (choosen.fi.fi >= choosen.fi.se){
        make_assert(choosen.se.fi, choosen.se.se, 0);
    } else{
        make_assert(choosen.se.fi, choosen.se.se, 1);
    }
}

int main () {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    cin >> n >> bombCnt;
    bomb.resize(n + 2, vector<bool>(n + 2, 0));
    mat.resize(n + 2, vector<int>(n + 2, 0));
    board.resize(n + 2, vector<int>(n + 2, -2));
    for (int i=1;i<=bombCnt;i++){
        string sa, sb;
        cin >> sa >> sb;
        int a = stoi(sa);
        int b = stoi(sb);
        bomb[a + 1][b + 1] = 1;
    }
    init();
    for (int i=1;i<=n;i++){
        for (int j=1;j<=n;j++){
            cout << mat[i][j] << " ";
        }
        cout << el;
    }

    make_assert(1, 1, 0);
    print_board();
    while (!selesai()){
        makeOneMove();
        print_board();
    }
    cout << "MENANG!!" << el;

    return 0;
}

/*
contoh input:
10
8
0, 6
2, 2
2, 4
3, 3
4, 2
5, 6
6, 2
7, 8
*/