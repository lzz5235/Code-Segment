#include <iostream>
#include <fstream>
#include <string>
#include <hash_map>
#include <algorithm>
#include<ctime>

using namespace std;
using namespace stdext;
typedef pair<std::string, int> Int_Pair;

void toLowerCase(string& str); 
int main()
{
		string temp;
		string word;
		stdext::hash_map <std::string, int> words;
		stdext::hash_map <std::string, int>::iterator wordsit;

		ifstream myfile("./document.txt");

		clock_t start,finish;
    	start=clock();

		if (myfile.is_open())
		{
			while ( myfile >> word )
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
					}
					else if( (word[word.length()-1]>'A' && word[word.length()-1] <'Z' )|| (word[word.length()-1]>'a' && word[word.length()-1]<'z'))
					{
						temp = temp.assign(word,0,word.length());
					}
					else
					{
						temp = temp.assign(word,0,word.length()-1);					
					}
					//cout << temp <<endl;
					
					wordsit = words.find(temp);
					
					if (wordsit != words.end())
						++(wordsit->second);
					else
					{
						words.insert( Int_Pair(temp,1) );
					}
			}
			myfile.close();
		}
		else
		{
			cout<<"Open Fail ......"<<endl;
			return 0;
		}


		std::vector < int > topvalue;
		int threshold = 0;
		for ( stdext::hash_map <std::string, int>::iterator wordsit = words.begin(); wordsit != words.end();wordsit++ )
		{
			topvalue.push_back( wordsit->second );
		}

		sort( topvalue.begin(), topvalue.end() );
		reverse( topvalue.begin(), topvalue.end() );

		if ( topvalue.size() > 10 )
		threshold = topvalue[9];

		finish=clock();
    	cout<<" Clock:   "<< (finish-start)/CLOCKS_PER_SEC<<endl;

		for ( stdext::hash_map <std::string, int>::iterator wordsit = words.begin(); wordsit != words.end();	wordsit++ )
		{
			if( wordsit->second >= threshold )
				cout << wordsit->first << "   " << wordsit->second<< endl;
		}
		return 0;
} 

void toLowerCase(string& str)
{
    for (int i = 0; i < str.length(); ++i)
        if (str[i] >= 'A' && str[i] <= 'Z')
             str[i] += ('a' - 'A');
}