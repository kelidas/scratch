#include <stdio.h>
#include <iostream> 
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <gmp.h>
#include <mpfr.h>
#include <assert.h>
//#include <conio.h>
using namespace std;
#include "BinomicLookup.h"

mpfr_t MPF_ZERO, MPF_ONE;

// Distribution function of one filament.
int Weibull(mpfr_t& weib_val,mpfr_t x, mpfr_t scale, mpfr_t shape, mpfr_rnd_t rnd){
	if (mpfr_cmp_ui(x, 0.0)<=0) {
        mpfr_set(weib_val,MPF_ZERO, rnd);
        return 0;
    };
    mpfr_set(weib_val,MPF_ZERO, rnd);
    mpfr_div (weib_val, x,scale,rnd);
	 mpfr_pow (weib_val, weib_val,shape,rnd);
    mpfr_neg (weib_val,weib_val,rnd);
    mpfr_exp (weib_val, weib_val,rnd);
    mpfr_sub (weib_val, MPF_ONE, weib_val, rnd);
    //mpfr_printf( "= %.1000Rg\n",weib_val);
    return 0;
}

// Recursion function. Distribution of the yarn strength.
int Gn(mpfr_t& gn_val,mpfr_t x, mpfr_t scale, mpfr_t shape, mpfr_t n, mpfr_rnd_t rnd){
// 	if( mpfr_cmp_ui(n, 1) < 0 ) {
//         mpfr_set(gn_val,MPF_ZERO, rnd);
//         mpfr_printf( "ted1 = %.1000Rg\n",gn_val);
//         return 0;
//     };
    mpfr_set(gn_val, MPF_ONE, rnd); 
    if( mpfr_cmp_ui(n, 1) == 0 ) {
        Weibull(gn_val, x, scale, shape, rnd);
        //mpfr_printf( "ted2 = %.100Rg\n",gn_val);
        return 0;
    };
    mpfr_t cdfx, vysl_1, vysl, cdfk, komb, new_x, new_d;
    mpfr_inits(cdfx, vysl_1, vysl, cdfk, komb, new_x, new_d, (mpfr_ptr) 0);
	//double vysl_1 = 0.0;
	//double cdf_k = 1.0;//pocatecni hodnota mocniny [ F(x) ]^k
	//double cdfx = Weibull(x, scale, shape, rnd);
    Weibull(cdfx, x, scale, shape, rnd);
	double komb_d;
    int n_int;
    n_int = mpfr_get_ui(n, rnd);
    mpfr_set(cdfk, MPF_ONE, rnd);
    mpfr_set(vysl, MPF_ZERO, rnd);

	for(int k = 1 ; k < n_int ; k++){
		mpfr_mul(cdfk, cdfk, cdfx, rnd); // cdf_k = [ F(x) ]^k
		komb_d = BinomicLookup[(n_int-1)*69 + k - 1];
		mpfr_set_d(komb, komb_d, rnd);
		if(( k%2 ) == 0) mpfr_neg(komb, komb, rnd);
        mpfr_mul(vysl_1, komb, cdfk, rnd);
        mpfr_sub_ui(new_d, n, k, rnd);
        mpfr_div(new_x, n, new_d, rnd);
        mpfr_mul(new_x, new_x, x, rnd);
        Gn(gn_val, new_x, scale, shape, new_d,rnd);
        mpfr_mul(vysl_1, vysl_1, gn_val, rnd);
        mpfr_add(vysl, vysl, vysl_1, rnd);
        //mpfr_printf( "ted = %.100Rg\n",gn_val);
	}

	mpfr_mul(cdfk, cdfk, cdfx, rnd); //cdf_k = [ Weibull(x) ]^n
    
	// k==n
	if(( n_int%2 ) == 0)	{ 
        mpfr_sub(vysl, vysl, cdfk, rnd);	
    }
	else				{ 
        mpfr_add(vysl, vysl, cdfk,rnd);	 
            }
    mpfr_set(gn_val, vysl, rnd);
    //mpfr_sub(gn_val, gn_val, vysl, rnd);
    mpfr_set(gn_val, vysl, rnd);
    
    mpfr_clears (cdfx, vysl_1, vysl, cdfk, komb, new_x, new_d, (mpfr_ptr) 0);
	//return vysl_1;
    return 0;
}

int main(){
    int inex;
    mpfr_set_default_prec(3325);
    mpfr_inits( MPF_ZERO, MPF_ONE, (mpfr_ptr) 0);
    inex = mpfr_set_str (MPF_ZERO, "0.0", 10, GMP_RNDN); assert (inex == 0);
    inex = mpfr_set_str (MPF_ONE, "1.0", 10, GMP_RNDN); assert (inex == 0);
    
    int i;
    int sims =  3000;
    double * X      = new double[sims]; //stress x (random variable)
    double * cdf_f  = new double[sims]; //actual cdf
    
    double xmultiple;

    double shape_in;
    double scale_in = 1.0;

    double pom=0.0;
    char pom_str[50];
    int vlaken_in;
    cout<<"Number of filaments: "; cin>>vlaken_in;
    cout<<"Weibull modulus (shape factor): ";   cin>>shape_in;

    mpfr_t x, scale, shape, weib_val, gn_val, vlaken, gn_ret;
    mpfr_inits (x, scale, shape, weib_val, gn_val, vlaken,gn_ret, (mpfr_ptr) 0);
    
    inex = mpfr_set_str (gn_val, "0.0",10, GMP_RNDN); assert (inex == 0);
    
    inex = mpfr_set_str (x, "2.1",10, GMP_RNDN); assert (inex == 0);
    sprintf(pom_str, "%f", scale_in);
    inex = mpfr_set_str (scale, pom_str ,10, GMP_RNDN); assert (inex == 0);
    sprintf(pom_str, "%f", shape_in);
    inex = mpfr_set_str (shape, pom_str,10, GMP_RNDN); assert (inex == 0);
    sprintf(pom_str, "%d", vlaken_in);
    inex = mpfr_set_str (vlaken, pom_str,10, GMP_RNDN); assert (inex == 0);
    mpfr_printf( "x = %.1000Rg\n",x);
    mpfr_printf( "scale = %.1000Rg\n",scale);
    mpfr_printf( "shape = %.1000Rg\n",shape);
    mpfr_printf( "n = %.1000Rg\n",vlaken);
    
    //Weibull(weib_val,x,scale,shape,GMP_RNDN);
    
    
    
    double start = clock();
    Gn(gn_val, x, scale, shape, vlaken, GMP_RNDN);
    double t = (clock() - start)/(double)CLOCKS_PER_SEC;
    cout << "time = " << t << endl;
    mpfr_printf( "gn = %.1000Rg\n",gn_val);
    
    //mpfr_t g,h,r;
    //mpfr_inits(g,h,r,(mpfr_ptr) 0);
    //inex = mpfr_set_str (g, "1.0",10, GMP_RNDN); assert (inex == 0);
    //inex = mpfr_set_str (h, "3.0",10, GMP_RNDN); assert (inex == 0);
    //mpfr_div(r,g,h,GMP_RNDN);
    //mpfr_printf( "gn = %.1000Rg\n",r);
    
    mpfr_clears (x, scale, shape, weib_val, gn_val, vlaken,gn_ret, (mpfr_ptr) 0);
    mpfr_clears (MPF_ZERO, MPF_ONE, (mpfr_ptr) 0);
    mpfr_free_cache ();
	
// 
// 	//double mu,std;
// 	//Get_Mean_Std_Gn(vlaken, scale, shape, &mu, &std);
// 	//cout << "mean:" << mu << "   std:" << std << endl;
// 
// 
// 	//	for(vlaken = 3;  vlaken < 4 ; vlaken ++){ 
// 		printf("n_f = %3i\n",vlaken);
// 
// 		//zapis na soubor
// 		char* filename = new char[50];
// 		sprintf(filename,"n=%02i_m=%.3f.txt",vlaken,shape);
// 		FILE * fCDF = fopen(filename, "w");
// 		//SOUBOR JE OTEVREN
// 		
// 		//hlavicka
// 		fprintf(fCDF," X \t cdf(x) \t ln(x) \t ln{-ln[1-cdf(x)]} \n\n");
// 
// 
// 
// 
// 		double lnxe = 0.03;
// 		double lnxb = 1/96.0*shape - 3.04;
// 		double krok = (lnxe-lnxb)/500;
// 		xmultiple = exp(krok);
// 
// 		
// 		
// 		
// 
// 		zac=clock();
// 
// 		//cyklus projizdi hodnoty "x" (sila) a pocita pro ne hodnotu distrib funkce pomoci Gn(x,n).
// 		for (x = exp(lnxb), i=0 ; i< sims, x<2 ; i++) {
// 			simSTART=clock();
// 			//vybere se jedna verze //vypocet phoenixovou rekurzi. Zvol verzi.
// 			//pom = Gn_Divided(x, scale, shape, vlaken); //verze s delenymi cykly
// 			pom = Gn(x, scale, shape, vlaken); //verze s jednim cyklem a rozlisenim "suda", licha
// 			simKONEC=clock();
// 			
// 			X[i]	 = x;//zapis do pole - x (sila)
// 			cdf_f[i] = pom;//zapis do pole - y = cdf(x)
// 				
// 			//obkrocne derivace:
// 			//cprintf("\rSimulace: %.i -- x=%.3f  -- %.3f s",i,x,(double)(simKONEC-simSTART)/CLOCKS_PER_SEC);
// 			if(pom>= 0.9999) break;//ukonceni pokud je Prst>= 0.9999. DAL MNE TO NEZAJIMA.
// 
// 
// 			//zapis dat na soubor
// 			if(i>0){
// 			fprintf(
// 					fCDF,"%.15e\t%.15e\t%.15e\t%.15e\n",	
// 					X[i-1]		, cdf_f[i-1] , log(X[i-1]), WeibPP(cdf_f[i-1])	
// 				   );
// 			}
// 			
// 			x *= xmultiple; //vypocet dalsi hodny sily, pro kterou chci Gn(x) = cdf_f
// 		}
// 		
// 		kon=clock();
// 		printf("\n");
// 		printf("--------------------");
// 		printf("\n");
// 
// 
// 		fclose(fCDF);
// 
// //	}
// 
// 	printf("\nVypocet - %.3f s\n",(double)(kon-zac)/CLOCKS_PER_SEC);
// 
// 
// 
// 	if(X)		delete[] X;			X=0;
// 	if(cdf_f)	delete[] cdf_f;		cdf_f=0;
    

return 0;
}






