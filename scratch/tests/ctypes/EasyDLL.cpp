// EasyDLL.cpp : Defines the entry point for the DLL application.
//

#include "stdafx.h"
#include "math.h"
#define M_PI 3.14159

//Function declarations
//extern "C" __declspec(dllexport) int __cdecl GetSphereSAandVol(double radius, double* sa, double* vol);
extern "C"  __declspec(dllexport) double __cdecl Multiply( double a, double b);
extern "C" __declspec(dllexport) double __cdecl Multiply_p( double a, double* b);
extern "C" __declspec(dllexport) int __cdecl Sum( int a, int b);

BOOL APIENTRY DllMain( HANDLE hModule, 
                       DWORD  dwReason, 
                       LPVOID lpReserved
					 )
{
    return TRUE;
}


__declspec(dllexport) double __cdecl Multiply( double a, double b){
	return a*b;
}


__declspec(dllexport) double __cdecl Multiply_p( double a, double* b){
	double c;
	c = a * *b;
	return c;
}

__declspec(dllexport) int __cdecl Sum( int a, int b){
	return a + b;
}