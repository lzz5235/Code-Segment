#include "stdafx.h"
#include "Base.h"

//��ʼ����̬��Ա����
int Base::count = 0;
//��̬����
int Base::instanceCount()
{
	cout<<"Base::instanceCount()\tcount��ַ�� " << &count << endl;
	return count;
}

Base::Base(int i)
{
	iBase = i;
	count++;
	cout<<"Base::Base()"<<endl;
}


Base::~Base(void)
{
	cout<<"Base::~Base()" <<endl;
}

int Base::getIBase() const
{
	cout<< "ʵ��iBase��ַ��" << &iBase << endl;
	return iBase;
}

void Base::print(void) const
{
	cout<<"Base::print()�� iBase " << iBase << endl;
}
