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
//-------------------------------------------------------
class MultiCore
{
	public:
		virtual void Show() = 0;
		virtual ~MultiCore(){};
};

class MultiCoreA:public MultiCore
{
	public:
		void Show()
		{
			cout<<"MultiCoreA"<<endl;
		}
};

class MultiCoreB:public MultiCore
{
    public:
        void Show()
        {   
            cout<<"MultiCoreB"<<endl;
        }   
};
//----------------------------------------------------------
class CoreFactory
{
	public:
		virtual SingleCore* CreateSingleCore() = 0;
		virtual MultiCore* CreateMultiCore() = 0;
};
class FactoryA:public CoreFactory
{
	public:
		SingleCore* CreateSingleCore()
		{
			return new CoreA();
		}
		MultiCore* CreateMultiCore()
		{
			return new MultiCoreA();
		}
};

class FactoryB:public CoreFactory
{
	public:
		SingleCore* CreateSingleCore()
		{
			return new CoreB();
		}
		MultiCore* CreateMultiCore()
		{
		    return new MultiCoreB();
		}

};


int main()
{
	FactoryA factorya;
	SingleCore  *pcorea = factorya.CreateSingleCore();
	pcorea->Show();

	MultiCore   *pmulticorea = factorya.CreateMultiCore();
	pmulticorea->Show();

	FactoryB factoryb;
	SingleCore  *pcoreb = factoryb.CreateSingleCore();
	pcoreb->Show();

	MultiCore   *pmulticoreb = factoryb.CreateMultiCore();
	pmulticoreb->Show();

	delete pcorea;
	delete pcoreb;
	delete pmulticorea;
	delete pmulticoreb;
}
