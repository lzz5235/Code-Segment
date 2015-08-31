#include <vector>
#include <iostream>
#include <string>
using namespace std;

class CCarModel
{
public:
    CCarModel(void) {}
    virtual ~CCarModel(void){}
    void Run()
    {
    	    vector<string>::const_iterator it = m_pSequence->begin();
	    for (; it < m_pSequence->end(); ++it)
	    {
	        string actionName = *it;
	        if(actionName.compare("start") == 0)
	        {
	            Start();
	        }
	        else if(actionName.compare("stop") == 0)
	        {
	            Stop();
	        }
	        else if(actionName.compare("alarm") == 0)
	        {
	            Alarm();
	        }
	        else if(actionName.compare("engine boom") == 0)
	        {
	            EngineBoom();
	        }
	    }
    }
    void SetSequence(vector<string> *pSeq)
    {
    		m_pSequence = pSeq;
    }
protected:
    virtual void Start() = 0;
    virtual void Stop() = 0;
    virtual void Alarm() = 0;
    virtual void EngineBoom() = 0;
private:
    vector<string> * m_pSequence;
};

class CBenzModel : public CCarModel
{
public:
    CBenzModel(void){}
    ~CBenzModel(void){}
protected:
    void Start(){cout << "Benz Start..." << endl;}
    void Stop(){cout << "Benz Stop..." << endl;}
    void Alarm(){cout << "Benz Alarm" << endl;}
    void EngineBoom(){cout << "Benz EngineBoom...." << endl;}
};

class CBMWModel : public CCarModel
{
public:
    CBMWModel(void){}
    ~CBMWModel(void){}
protected:
    void Start(){cout << "BMW Start..." << endl;}
    void Stop(){cout << "BMW Stop..." << endl;}
    void Alarm(){cout << "BMW Alarm" << endl;}
    void EngineBoom(){cout << "BMW EngineBoom...." << endl;}
};

class ICarBuilder
{
public:
    ICarBuilder(void)   { }
    virtual ~ICarBuilder(void)  { }
    virtual void SetSequence(vector<string> *pseq) = 0;
    virtual CCarModel * GetCarModel() = 0;
};

class CBenzBuilder : public ICarBuilder
{
public:
    CBenzBuilder(void);
    ~CBenzBuilder(void);
    void SetSequence(vector<string> *pSeq);
    CCarModel * GetCarModel();
private:
    CCarModel *m_pBenz;
};
CBenzBuilder::CBenzBuilder(void)
{
    m_pBenz = new CBenzModel();
}
CBenzBuilder::~CBenzBuilder(void)
{
    delete m_pBenz;
}
void CBenzBuilder::SetSequence(vector<string> *pSeq)
{
    m_pBenz->SetSequence(pSeq);
}
CCarModel * CBenzBuilder::GetCarModel()
{
    return m_pBenz;
}

class CBMWBuilder :public ICarBuilder
{
public:
    CBMWBuilder(void);
    ~CBMWBuilder(void);
    void SetSequence(vector<string> *pSeq);
    CCarModel * GetCarModel();
private:
    CCarModel *m_pBMW;
};

CBMWBuilder::CBMWBuilder(void)
{
    m_pBMW = new CBMWModel();
}
CBMWBuilder::~CBMWBuilder(void)
{
    delete m_pBMW;
}
void CBMWBuilder::SetSequence( vector<string> *pSeq )
{
    m_pBMW->SetSequence(pSeq);
}
CCarModel * CBMWBuilder::GetCarModel()
{
    return m_pBMW;
}

class CDirector
{
public:
    CDirector(void);
    ~CDirector(void);
    CBenzModel * GetABenzModel();
    CBenzModel * GetBBenzModel();
    CBMWModel * GetCBMWModel();
    CBMWModel * GetDBMWModel();
private:
    vector<string> * m_pSeqence;
    CBenzBuilder * m_pBenzBuilder;
    CBMWBuilder * m_pBMWBuilder;
};

CDirector::CDirector(void)
{
    m_pBenzBuilder = new CBenzBuilder();
    m_pBMWBuilder = new CBMWBuilder();
    m_pSeqence = new vector<string>();
}
CDirector::~CDirector(void)
{
    delete m_pBenzBuilder;
    delete m_pBMWBuilder;
    delete m_pSeqence;
}
CBenzModel * CDirector::GetABenzModel()
{
    m_pSeqence->clear();
    m_pSeqence->push_back("start");
    m_pSeqence->push_back("stop");
    m_pBenzBuilder->SetSequence(m_pSeqence);
    return dynamic_cast<CBenzModel*>(m_pBenzBuilder->GetCarModel());
}
CBenzModel * CDirector::GetBBenzModel()
{
    m_pSeqence->clear();
    m_pSeqence->push_back("engine boom");
    m_pSeqence->push_back("start");
    m_pSeqence->push_back("stop");
    m_pBenzBuilder->SetSequence(m_pSeqence);
    return dynamic_cast<CBenzModel*>(m_pBenzBuilder->GetCarModel());
}
CBMWModel * CDirector::GetCBMWModel()
{
    m_pSeqence->clear();
    m_pSeqence->push_back("alarm");
    m_pSeqence->push_back("start");
    m_pSeqence->push_back("stop");
    m_pBMWBuilder->SetSequence(m_pSeqence);
    return static_cast<CBMWModel*>(m_pBMWBuilder->GetCarModel());
}
CBMWModel * CDirector::GetDBMWModel()
{
    m_pSeqence->clear();
    m_pSeqence->push_back("start");
    m_pBenzBuilder->SetSequence(m_pSeqence);
    return dynamic_cast<CBMWModel*>(m_pBMWBuilder->GetCarModel());
}
int main(int argc, char const *argv[])
{
	CDirector *dir = new CDirector();

	dir->GetBBenzModel()->Run();
	return 0;
}