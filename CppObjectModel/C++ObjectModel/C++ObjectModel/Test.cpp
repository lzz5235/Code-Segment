// C++ObjectModel.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "Base.h"
#include "Derived.h"
#include "Derived_Overrite.h"
#include "Derived_Mutlip_Inherit.h"
#include "Derived_Virtual_Inherit1.h"
#include "Derived_Virtual.h"
#include "type_info.h"
#include <windows.h>
#include <iostream>
#include <string>
using namespace std;

void test_base_model(void);
void test_single_inherit_norewrite(void);
void test_single_inherit_rewrite(void);
void test_multip_inherit(void);
void test_single_vitrual_inherit(void);
void test_multip_vitrual_inherit(void);

void test_polymorphisn(void);

int _tmain(int argc, _TCHAR* argv[])
{
	while (true)
	{
		SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_GREEN);
		cout << "C++����ģ�Ͳ��Գ����������Ӧ�Ĳ��Ժţ�(����0�˳�)\n";
		cout << "\t1.���Ի�������ģ��\n";
		cout << "\t2.���Ե��̳ж���ģ�ͣ����ޡ���д������\n";
		cout << "\t3.���Ե��̳ж���ģ�ͣ����С���д������\n";
		cout << "\t4.���Զ�̳ж���ģ��\n";
		cout << "\t5.���Ե�һ��̳ж���ģ��\n";
		cout << "\t6.���������ظ���̳ж���ģ��\n";

		SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED); 
		int test_no;
		cout << "�����룺";
		cin >> test_no;
		cout << "��ѡ��Ĳ��Ժ��ǣ�" << test_no << endl;
		switch (test_no)
		{
		case 0://�˳�
			exit(0);
			break;
		case 1://1.���Ի�������ģ��
			test_base_model();
			break;
		case 2://2.���Ե��̳ж���ģ�ͣ����ޡ���д������
			test_single_inherit_norewrite();
			break;
		case 3://3.���Ե��̳ж���ģ�ͣ����С���д������
			test_single_inherit_rewrite();
			break;
		case 4://4.���Զ�̳ж���ģ��
			test_multip_inherit();
			break;
		case 5://5.���Ե�һ��̳ж���ģ��
			test_single_vitrual_inherit();
			break;
		case 6://6.���������ظ���̳ж���ģ��
			test_multip_vitrual_inherit();
			break;
		default:
			cout << "������ԺŴ���" << endl;
			break;
		}
	}

	return 0;
}

void test_base_model()
{
	Base b1(1000);
	cout << "����b1����ʼ�ڴ��ַ��" << &b1 << endl;
	cout << "type_info��Ϣ��" << ((int*)*(int*)(&b1) - 1) << endl;
	RTTICompleteObjectLocator str=
		*((RTTICompleteObjectLocator*)*((int*)*(int*)(&b1) - 1));
	//abstract class name from RTTI
	string classname(str.pTypeDescriptor->name);
	classname = classname.substr(4,classname.find("@@")-4);
	cout << classname <<endl;
	cout << "�麯�����ַ��\t\t\t" << (int*)(&b1) << endl;
	cout << "�麯���� �� ��1��������ַ��\t" << (int*)*(int*)(&b1) << "\t������������ַ��" << (int*)*((int*)*(int*)(&b1)) << endl;
	cout << "�麯���� �� ��2��������ַ��\t" << ((int*)*(int*)(&b1) + 1) << "\t";
	typedef void(*Fun)(void);
	Fun pFun = (Fun)*(((int*)*(int*)(&b1)) + 1);
	pFun();
	b1.print();
	cout << endl;
	cout << "�Ʋ����ݳ�ԱiBase��ַ��\t\t" << ((int*)(&b1) +1) << "\tͨ����ַȡֵiBase��ֵ��" << *((int*)(&b1) +1) << endl;
	cout << "Base::getIBase(): " << b1.getIBase() << endl;

	b1.instanceCount();
	cout << "��̬����instanceCount��ַ�� " << b1.instanceCount << endl;
}

void test_single_inherit_norewrite()
{
	Derived d(9999);
	cout << "����d����ʼ�ڴ��ַ��" << &d << endl;
	cout << "type_info��Ϣ��" << ((int*)*(int*)(&d) - 1) << endl;
	RTTICompleteObjectLocator str=
		*((RTTICompleteObjectLocator*)*((int*)*(int*)(&d) - 1));
	//abstract class name from RTTI
	string classname(str.pTypeDescriptor->name);
	classname = classname.substr(4,classname.find("@@")-4);
	cout << classname <<endl;
	cout << "�麯�����ַ��\t\t\t" << (int*)(&d) << endl;
	cout << "�麯���� �� ��1��������ַ��\t" << (int*)*(int*)(&d) << "\t������������ַ" << endl;
	cout << "�麯���� �� ��2��������ַ��\t" << ((int*)*(int*)(&d) + 1) << "\t";
	typedef void(*Fun)(void);
	Fun pFun = (Fun)*(((int*)*(int*)(&d)) + 1);
	pFun();
	d.print();
	cout << endl;

	cout << "�麯���� �� ��3��������ַ��\t" << ((int*)*(int*)(&d) + 2) << "\t";
	pFun = (Fun)*(((int*)*(int*)(&d)) + 2);
	pFun();
	d.derived_print();
	cout << endl;

	cout << "�Ʋ����ݳ�ԱiBase��ַ��\t\t" << ((int*)(&d) +1) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&d) +1) << endl;
	cout << "�Ʋ����ݳ�ԱiDerived��ַ��\t" << ((int*)(&d) +2) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&d) +2) << endl;
}

void test_single_inherit_rewrite()
{
	Derived_Overrite d(111111);
	cout << "����d����ʼ�ڴ��ַ��\t\t" << &d << endl;
	cout << "�麯�����ַ��\t\t\t" << (int*)(&d) << endl;
	cout << "�麯���� �� ��1��������ַ��\t" << (int*)*(int*)(&d) << "\t������������ַ" << endl;
	cout << "�麯���� �� ��2��������ַ��\t" << ((int*)*(int*)(&d) + 1) << "\t";
	typedef void(*Fun)(void);
	Fun pFun = (Fun)*(((int*)*(int*)(&d)) + 1);
	pFun();
	d.print();
	cout << endl;

	cout << "�麯���� �� ��3��������ַ��\t" << *((int*)*(int*)(&d) + 2) << "��������\t";
	cout << endl;

	cout << "�Ʋ����ݳ�ԱiBase��ַ��\t\t" << ((int*)(&d) +1) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&d) +1) << endl;
	cout << "�Ʋ����ݳ�ԱiDerived��ַ��\t" << ((int*)(&d) +2) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&d) +2) << endl;
}

void test_multip_inherit()
{
	Derived_Mutlip_Inherit dmi(3333);
	cout << "����dmi����ʼ�ڴ��ַ��\t\t" << &dmi << endl;
	cout << "�麯����_vptr_Base��ַ��\t" << (int*)(&dmi) << endl;
	cout << "_vptr_Base �� ��1��������ַ��\t" << (int*)*(int*)(&dmi) << "\t������������ַ" << endl;
	cout << "_vptr_Base �� ��2��������ַ��\t" << ((int*)*(int*)(&dmi) + 1) << "\t";
	typedef void(*Fun)(void);
	Fun pFun = (Fun)*(((int*)*(int*)(&dmi)) + 1);
	pFun();
	cout << endl;
	cout << "_vptr_Base �� ��3��������ַ��\t" << ((int*)*(int*)(&dmi) + 2) << "\t";
	pFun = (Fun)*(((int*)*(int*)(&dmi)) + 2);
	pFun();
	cout << endl;
	cout << "_vptr_Base �� ��4��������ַ��\t" << *((int*)*(int*)(&dmi) + 3) << "��������\t";
	cout << endl;
	cout << "�Ʋ����ݳ�ԱiBase��ַ��\t\t" << ((int*)(&dmi) +1) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dmi) +1) << endl;


	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_GREEN); 
	cout << "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED); 
	cout << "�麯����_vptr_Base1��ַ��\t" << ((int*)(&dmi) +2) << endl;
	cout << "_vptr_Base1 �� ��1��������ַ��\t" << (int*)*((int*)(&dmi) +2) << "\t������������ַ" << endl;
	cout << "_vptr_Base1 �� ��2��������ַ��\t" << ((int*)*((int*)(&dmi) +2) + 1) << "\t";
	typedef void(*Fun)(void);
	pFun = (Fun)*((int*)*((int*)(&dmi) +2) + 1);
	pFun();
	cout << endl;
	cout << "_vptr_Base1 �� ��3��������ַ��\t" << *((int*)*(int*)((int*)(&dmi) +2) + 2) << "��������\t";
	cout << endl;	
	cout << "�Ʋ����ݳ�ԱiBase1��ַ��\t" << ((int*)(&dmi) +3) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dmi) +3) << endl;
	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_GREEN); 
	cout << "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED); 
	cout << "�Ʋ����ݳ�ԱiDerived��ַ��\t" << ((int*)(&dmi) +4) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dmi) +4) << endl;
}

void test_single_vitrual_inherit()
{
	Derived_Virtual_Inherit1 dvi1(88888);
	cout << "����dvi1����ʼ�ڴ��ַ��\t\t" << &dvi1 << endl;
	cout << "�麯����_vptr_Derived..��ַ��\t\t" << (int*)(&dvi1) << endl;
	cout << "_vptr_Derived �� ��1��������ַ��\t" << (int*)*(int*)(&dvi1) << endl;
	typedef void(*Fun)(void);
	Fun pFun = (Fun)*((int*)*(int*)(&dvi1));
	pFun();
	cout << endl;
	cout << "_vptr_Derived �� ��2��������ַ��\t" << *((int*)*(int*)(&dvi1) + 1) << "��������\t";
	cout << endl;
	cout << "=======================��\t" << ((int*)(&dvi1) +1) << "\tͨ����ַȡ�õ�ֵ��" << (int*)*((int*)(&dvi1) +1) << "\t" <<*(int*)*((int*)(&dvi1) +1) << endl;
	cout << "�Ʋ����ݳ�ԱiDerived��ַ��\t" << ((int*)(&dvi1) +2) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dvi1) +2) << endl;
	cout << "=======================��\t" << ((int*)(&dvi1) +3) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dvi1) +3) << endl;
	cout << "�麯����_vptr_Base��ַ��\t" << ((int*)(&dvi1) +4) << endl;
	cout << "_vptr_Base �� ��1��������ַ��\t" << (int*)*((int*)(&dvi1) +4) << "\t������������ַ" << endl;
	cout << "_vptr_Base �� ��2��������ַ��\t" << ((int*)*((int*)(&dvi1) +4) +1) << "\t";
	pFun = (Fun)*((int*)*((int*)(&dvi1) +4) +1);
	pFun();
	cout << endl;
	cout << "_vptr_Base �� ��3��������ַ��\t" << ((int*)*((int*)(&dvi1) +4) +2) << "��������\t" << *((int*)*((int*)(&dvi1) +4) +2);
	cout << endl;
	cout << "�Ʋ����ݳ�ԱiBase��ַ��\t\t" << ((int*)(&dvi1) +5) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dvi1) +5) << endl;
}

void test_multip_vitrual_inherit()
{
	Derived_Virtual dvi1(88888);
	cout << "����dvi1����ʼ�ڴ��ַ��\t\t" << &dvi1 << endl;
	cout << "�麯����_vptr_inherit1��ַ��\t\t" << (int*)(&dvi1) << endl;
	cout << "_vptr_inherit1 �� ��1��������ַ��\t" << (int*)*(int*)(&dvi1) << endl;
	typedef void(*Fun)(void);
	Fun pFun = (Fun)*((int*)*(int*)(&dvi1));
	pFun();
	cout << endl;
	cout << "_vptr_inherit1 �� ��2��������ַ��\t" << ((int*)*(int*)(&dvi1) + 1) << endl;
	pFun = (Fun)*((int*)*(int*)(&dvi1) + 1);
	pFun();
	cout << endl;
	cout << "_vptr_inherit1 �� ��3��������ַ��\t" << ((int*)*(int*)(&dvi1) + 2) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)*(int*)(&dvi1) + 2) << "��������\t";
	cout << endl;
	cout << "======ָ��=============��\t" << ((int*)(&dvi1) +1) << "\tͨ����ַȡ�õ�ֵ��" << (int*)*((int*)(&dvi1) +1)<< "\t" <<*(int*)*((int*)(&dvi1) +1) << endl;
	cout << "�Ʋ����ݳ�ԱiInherit1��ַ��\t" << ((int*)(&dvi1) +2) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dvi1) +2) << endl;
	//
	cout << "�麯����_vptr_inherit2��ַ��\t" << ((int*)(&dvi1) +3) << endl;
	cout << "_vptr_inherit2 �� ��1��������ַ��\t" << (int*)*((int*)(&dvi1) +3) << endl;
	pFun = (Fun)*((int*)*((int*)(&dvi1) +3));
	pFun();
	cout << endl;
	cout << "_vptr_inherit2 �� ��2��������ַ��\t" << (int*)*((int*)(&dvi1) +3) + 1 <<"\tͨ����ַȡ�õ�ֵ��" << *((int*)*((int*)(&dvi1) +3) + 1) << "��������\t" << endl;
	cout << endl;
	cout << "======ָ��=============��\t" << ((int*)(&dvi1) +4) << "\tͨ����ַȡ�õ�ֵ��" << (int*)*((int*)(&dvi1) +4) << "\t" <<*(int*)*((int*)(&dvi1) +4)<< endl;
	cout << "�Ʋ����ݳ�ԱiInherit2��ַ��\t" << ((int*)(&dvi1) +5) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dvi1) +5) << endl;
	cout << "�Ʋ����ݳ�ԱiDerived��ַ��\t" << ((int*)(&dvi1) +6) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dvi1) +6) << endl;
	cout << "=======================��\t" << ((int*)(&dvi1) +7) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dvi1) +7) << endl;
	//
	cout << "�麯����_vptr_Base��ַ��\t" << ((int*)(&dvi1) +8) << endl;
	cout << "_vptr_Base �� ��1��������ַ��\t" << (int*)*((int*)(&dvi1) +8) << "\t������������ַ" << endl;
	cout << "_vptr_Base �� ��2��������ַ��\t" << ((int*)*((int*)(&dvi1) +8) +1) << "\t";
	pFun = (Fun)*((int*)*((int*)(&dvi1) +8) +1);
	pFun();
	cout << endl;
	cout << "_vptr_Base �� ��3��������ַ��\t" << ((int*)*((int*)(&dvi1) +8) +2) << "��������\t" << *((int*)*((int*)(&dvi1) +8) +2);
	cout << endl;
	cout << "�Ʋ����ݳ�ԱiBase��ַ��\t\t" << ((int*)(&dvi1) +9) << "\tͨ����ַȡ�õ�ֵ��" << *((int*)(&dvi1) +9) << endl;
}

void test_polymorphisn()
{
	
}
