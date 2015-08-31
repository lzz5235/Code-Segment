//输入单词，统计单词出现次数并按照单词出现次数从多到少排序
#include <cstdlib>
#include <map>
#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include <fstream>
#include<ctime>

using namespace std;
 
void sortMapByValue(map<std::string, int>& tMap, vector<std::pair<std::string, int> >& tVector);
int cmp(const pair<string, int>& x, const pair<string, int>& y);
void toLowerCase(string& str); 


int main()
{
		string word,temp;
		fstream myfile;
		myfile.open("./document.txt",ios::in);
		
		map<std::string, int> tMap;
		pair< map<  string, int>::iterator, bool> ret;
		
		clock_t start,finish;
    	start=clock();
		
		if (myfile.is_open())
		{
			while (myfile >> word)
			{
				toLowerCase(word);
				if(word == "at" || word == "me"|| word == "him" || word == "she"|| word == "the" || word == "The"|| word =="and" || word == "I" || word == "i"|| word =="to" || word=="of" || word =="a" ||word=="in"
						||word =="was" ||word =="that" ||word =="had"  || word =="he" || word =="you" 
							|| word=="his" || word =="my" ||word=="it" ||word =="as" || word =="with" ||
								word =="her" || word =="for" || word=="on" )
								{
									continue;
								}
				if(word[word.length()-2]=='\'' )
				{
					temp = temp.assign(word,0,word.length()-3);
					ret = tMap.insert( make_pair(temp, 1));
				}
				else if( (word[word.length()-1]>'A' && word[word.length()-1] <'Z' )|| (word[word.length()-1]>'a' && word[word.length()-1]<'z'))
				{
					ret = tMap.insert( make_pair(word, 1));
				}
				else
				{
					temp = temp.assign(word,0,word.length()-1);
					ret = tMap.insert( make_pair(temp, 1));
					
				}		
			   if (!ret.second)
			        ++ret.first->second;
			}
			myfile.close();
		}
		else
		{
					cout<< "Open fail!"<<endl;
				return 0;			
		}
		
		vector< pair< string,int> > tVector;
		sortMapByValue(tMap,tVector);
		
		finish=clock();
    	cout<<" Clock:   "<< (finish-start)/CLOCKS_PER_SEC<<endl;
    	
		for(int i=0;i<10;i++)//前10个， tVector.size()
		{
			 cout<<tVector[i].first<<": "<<tVector[i].second<< endl;
		}  
 
		 system("pause");
		 return 0;
}
 
int cmp(const pair<string, int>& x, const pair<string, int>& y)
{
 	return x.second > y.second;
}
 
void sortMapByValue(map<string, int>& tMap, vector<pair<string, int> >& tVector)
{
	 for (map<string, int>::iterator curr = tMap.begin(); curr != tMap.end(); curr++)
	 {
	 		tVector.push_back(make_pair(curr->first, curr->second));
	 }
	 
	 sort(tVector.begin(), tVector.end(), cmp);
}
void toLowerCase(string& str)
{
    for (int i = 0; i < str.length(); ++i)
        if (str[i] >= 'A' && str[i] <= 'Z')
             str[i] += ('a' - 'A');
}