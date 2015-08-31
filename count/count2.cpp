#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <cctype>
using namespace std;

 
void toLowerCase(string& str)
{
    for (int i = 0; i < str.length(); ++i)
        if (str[i] >= 'A' && str[i] <= 'Z')
             str[i] += ('a' - 'A');
}

int main(int argc,char*argv[])
{
	string word,temp;
	map <string, int > freq;
	map <string, int >::const_iterator wordsit;
	fstream myfile;
	myfile.open("./document.txt",ios::in);
	
	// Load file into string
	if (myfile.is_open())
	{
		while (myfile >> word)
		{
			toLowerCase(word);
			if(word == "the" || word == "The"|| word =="and" || word == "I" || word =="to" || word=="of" || word =="a" ||word=="in"
					||word =="was" ||word =="that" ||word =="had"  || word =="he" || word =="you" 
						|| word=="his" || word =="my" ||word=="it" ||word =="as" || word =="with" ||
							word =="her" || word =="for" || word=="on" )
							{
								continue;
							}
			if(word[word.length()-2]=='\'' )
			{
				temp = temp.assign(word,0,word.length()-3);
				freq[temp]++;
			}
			else if( (word[word.length()-1]>'A' && word[word.length()-1] <'Z' )|| (word[word.length()-1]>'a' && word[word.length()-1]<'z'))
			{
				freq[word]++;
			}
			else
			{
				temp = temp.assign(word,0,word.length()-1);
				freq[temp]++;
			}		
		}
		myfile.close();
	}
	else
	{
		cout<< "Open fail!"<<endl;
		return 0;
	}
	
	
	//To see the map created
	for (wordsit=freq.begin();wordsit!=freq.end();wordsit++)
	{	
		cout<<"Key: "<<wordsit->first<<"       Value:"<<wordsit->second<<endl;
	}
} 