#include <bits/stdc++.h>
#include <queue>
#include <string>
using namespace std;

#define N 8

vector<vector<string>> goals; //initializing list of goals and non-attacking states
vector<vector<string>> non_attacking_states;
int sol=0;
int cnt = 1;

//function to print the board
void print(vector<string>& state){
	for (auto& str : state){
		for (auto& letter : str){
            cout << letter << " ";
        }
		cout << endl;
	}
	return;
}

//function to check if a state is safe(non-attacking)
bool safe(int r, int c, vector<string>& board){
    for(int i=0;i<board.size();i++){
        if(board[i][c] == 'Q'){
            return false;
        }
    }

	int i = r; 
    int j = c;
	while(i >= 0 && j >= 0){
        if(board[i--][j--] == 'Q'){
            return false;
        }
    }
			
	i = r;
    j = c;
	while(i >= 0 && j < board.size()){
        if(board[i--][j++] == 'Q'){
            return false;
        }
    }	
	return true;
}

bool goal(vector<string> state, int r){    
    if(r == N ){
        return true;
    }
    return false;
}

//function to get list of succeeding states
vector<vector<string>> succ(vector<string> state, int r){
    vector<string> str;
    vector<vector<string>> succ_states; //list containing succeeding safe states
    for(int i = 0; i < N; i++){
        str = state;
        if(safe(r, i, state)){
            str[r][i] = 'Q';
            succ_states.push_back(str);
            cnt++;
            non_attacking_states.push_back(str);
        }
    }
    return succ_states;
}

void search_tree(vector<string>& state, int r){
    queue<vector<string>> open;    
    queue<int> row;      
    vector<vector<string>> succ_state;
    
    if(!goal(state, r)){
        open.push(state);
        row.push(r);
    }

    // creating the search tree
    vector<string> s;
    while(open.size()){   
        // breadth-first search
        s = open.front();   
        open.pop();
        if(goal(s, row.front())){
            sol++;
            goals.push_back(s);
        }
        r = row.front();
        row.pop();
        if(r < N){        
            succ_state = succ(s,r++);  
            for(int i = 0 ; i < succ_state.size(); i++){
                open.push(succ_state[i]);
                row.push(r);
            }
        }
    }
}

// enter 1 to view all the goal states

int main(){
    vector<string> state;
    string s;
    for(int i = 0 ; i < N ; i++){
        s += ".";
    }
    for(int i = 0; i < N; i++){
        state.push_back(s);
    }
   
    search_tree(state, 0);
    int x;
    cin>>x;

    if(x == 1){
        for(int i = 0; i < goals.size(); i++){
        print(goals[i]);
        cout<<endl;
        }
    }
    cout<<"no. of solutions :"<<sol<<endl;
    cout<<"no. of non-attacking states :"<<cnt<<endl;
}