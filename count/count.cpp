#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>
#include <map>
using namespace std;


int main()
{
	string line, file;
	std::map <std::string, int> words;
	std::map <std::string, int>::iterator wordsit;
	ifstream myfile("./document.txt");


	if (myfile.is_open())
	{
		while (! myfile.eof() )
		{
			getline(myfile,line);
			file.append( line );
			file.append( " " );
		}
		myfile.close();
	}
	
	char * threadsafe;
	char * token = strtok((char*)file.c_str(), " ");
	while (token != NULL)
	{
		wordsit = words.find(token);
		if (wordsit != words.end())
			++wordsit->second;
		else
			words[token] = 1;
		
		token = strtok(NULL, " ");
	}
	
	// find top 10 threshold value
	std::vector < int > topvalue;
	int threshold = 0;
	for ( wordsit = words.begin(); wordsit != words.end();
	wordsit++ )
	{
		topvalue.push_back( wordsit->second );
	}
	sort( topvalue.begin(), topvalue.end() );
	reverse( topvalue.begin(), topvalue.end() );
	
	if ( topvalue.size() > 10 )
	threshold = topvalue[9];
	
	// Search hashmap against value and print word if its
	//within top10 threshold... 
	// ties also get printed, so the list might be longer than 10
	for ( wordsit = words.begin(); wordsit != words.end();
	wordsit++ )
	{
		if( wordsit->second >= threshold )
		cout << wordsit->first << endl;
	}
	return 0;
} 