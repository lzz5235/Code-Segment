#include <iostream>
using namespace std;

enum TYPE{COREA,COREB};



class SingleCore
{
	public:
		virtual ~SingleCore(){};
		virtual void Show() = 0;
};

class CoreA:public SingleCore
{
	public:
		void Show()
		{
			cout<< "CoreA"<<endl;
		}
};
class CoreB:public SingleCore
{
	public:
		void Show()
		{
			cout <<"CoreB"<<endl;
		}
};

class SingleFactory
{
	public:
		SingleCore* CreateSingleCore(enum TYPE type)
		{
			if(type==COREA)
				return new CoreA();
			else if(type==COREB)
				return new CoreB();
			else 
				return NULL;
		}
};


int main()
{
	SingleFactory factory;
	SingleCore  *pcorea = factory.CreateSingleCore(COREA);
	pcorea->Show();
	SingleCore  *pcoreb = factory.CreateSingleCore(COREB);
	pcoreb->Show();

	delete pcorea;
	delete pcoreb;
}
