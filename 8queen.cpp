#include<bits/stdc++.h>
#include<vector>
#include<queue>
using namespace std;

#define N 8
int sol;
int cnt;

struct state{
    int board[N][N];
    vector<state> next;
};

bool safe(struct state* a, int col, int row){
    for(int i=0;i<N;i++){
        if(a->board[i][col]){
            return false;
        }
    }
    int j = col;
    int i = row;

    while(i>=0 && j>=0){
        if(a->board[i--][j--]){
            return false;
        }
    }
    
    i = row;
    j = col;
    while(i>=0 && j<N){
        if(a->board[i--][j++]){
            return false;
        }
    }
    return true;
}

void display(struct state a){
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            if(a.board[i][j]==1){
                cout<<"Q ";
            }
            else{
                cout<<". ";
            }
        }
        cout<<endl;
    }
    cout<<endl;
}

// function that returns the vector of next nodes of graph
vector<state> get_nxt(struct state a, int row){
    vector<state> x;
    for(int i=0;i<N;i++){
        state *ad = new struct state;
        for(int k=0;k<N;k++){
            for(int j=0;j<N;j++){
                ad->board[k][j] = a.board[k][j];
            }
        }
        if(safe(ad,i,row)){
            ad->board[row][i] = 1;
            cnt++;
            x.push_back(*ad);
        }
        free(ad);
    }
    return x;
}

void search(state a){
    int r = 0;
    queue<int> row;
    queue<state> st;
    st.push(a);
    row.push(r);
    while(!st.empty()){
        state s = st.front();
        if(row.front() == N){
            sol++;
            display(s);
        }
        st.pop();
        r = row.front();
        row.pop();
        if(r<N){
            vector<state> ne = get_nxt(s,r++);
            //cout<<ne.size()<<endl;
            for(auto i = ne.begin();i!=ne.end();i++){
                st.push(*i);
                row.push(r);
            }
        }
    }
}

int main(){
    struct state init;
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            init.board[i][j] = 0;
        }
    }
    //display(init);
    cout<<"solution boards are:"<<endl;
    search(init);
    cout<<"number of solutions: "<<sol<<endl;
    cout<<"number of non-attacking states: "<<cnt<<endl;
}
