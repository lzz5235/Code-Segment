#include <iostream>
using namespace std;


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
		virtual SingleCore* CreateSingleCore() = 0;
};
class FactoryA:public SingleFactory
{
	public:
		SingleCore* CreateSingleCore()
		{
			return new CoreA;
		}
};

class FactoryB:public SingleFactory
{
	public:
		SingleCore* CreateSingleCore()
		{
			return new CoreB;
		}
};


int main()
{
	FactoryA factorya;
	SingleCore  *pcorea = factorya.CreateSingleCore();
	pcorea->Show();

	FactoryB factoryb;
	SingleCore  *pcoreb = factoryb.CreateSingleCore();
	pcoreb->Show();

	delete pcorea;
	delete pcoreb;
}
