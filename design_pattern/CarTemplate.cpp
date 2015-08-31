#include <iostream>
using namespace std;

class CarTemplate
{
public:
	CarTemplate(void){};
    virtual ~CarTemplate(void){};

protected:
    virtual void Start() = 0;
    virtual void Stop() = 0;
    virtual void Alarm() = 0;
    virtual void EngineBoom() = 0;
    virtual bool IsAlarm() =0;

public:
    	void Run()
    	{
		Start();

		EngineBoom();
		
		if(IsAlarm())
			Alarm();

		Stop();
    	};
};

class Hummer: public CarTemplate
{
public:
	Hummer(){m_isAlarm = true;}
	virtual ~Hummer(){};
	

protected:
	void Start(){	cout<< "Hummer Start" <<endl;	}
	void Stop(){	cout<< "Hummer Stop" <<endl;	}
	void Alarm(){	cout<< "Hummer Alarm" <<endl;}
	bool IsAlarm(){	return m_isAlarm;		}
	void EngineBoom(){	cout<< "Hummer EngineBoom" <<endl;	}
private:
    bool m_isAlarm;
};

class Benz: public CarTemplate
{
public:
	Benz(){m_isAlarm = false;}
	virtual ~Benz(){};

protected:
	void Start(){	cout<< "Benz Start" <<endl;	}
	void Stop(){	cout<< "Benz Stop" <<endl;	}
	void Alarm(){	cout<< "Benz Alarm" <<endl;}
	bool IsAlarm(){	return m_isAlarm;		}
	void EngineBoom(){	cout<< "Benz EngineBoom" <<endl;	}
private:
    bool m_isAlarm;
};

int main()
{
	CarTemplate *hummer = new Hummer();
	hummer->Run();
	delete  hummer;

	CarTemplate *benz = new Benz();
	benz->Run();
	delete benz;
}