/*
 # Made by:
 # Sergio Mendoza <sergio@astro.unam.mx>
 # Gustavo Magallanes-Guijón <gustavo.magallanes.guijon@ciencias.unam.mx>
 # Instituto de Astronomia UNAM
 # Ciudad Universitaria
 # Ciudad de Mexico
 # Mexico
 #
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
/* The following is included by gsl_math.h */
/* #include <math.h> */
#include <gsl/gsl_math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_sf_result.h>
#include <gsl/gsl_sf_elljac.h>
#include <gsl/gsl_sf_ellint.h>
#include <time.h>

/* This opens the functions to be read and written */
void openfiles() ;
/* This closes the function to be written out */
void closefiles();
/* This writes out to the *datafile pointer */
void loop();
void loopT();
/* Function to calculate likelihood  */
void likelihood(double, double, double, double, double, double);//, int);

double randfrom(double, double); 

/*Count of lines in file*/
int lines_input = 11849;
// First entrance is time and second is number of parameters of Likelihood
// Correct the following!
double matrixdata[1000000][10];
double matriz[1000000][2];
double nueva_matriz[1000000][2];

double step(double);

double jacobi(double, double, double, double, double, double, double, double);

/* Datafile to be open */
FILE *datafilewrite;
FILE *datafileread;

int main()
{
	openfiles();
	loop();
	loopT() ;
	closefiles();
	
	return 0;
}

void loop()
{
double  tobs, Lth, sigma ;

for(int m = 0; m < lines_input; m++){
    fscanf(datafileread, "%lf %lf %lf", &tobs, &Lth, &sigma);
    matrixdata[m][1] = tobs ;
    matrixdata[m][2] = Lth ;
    matrixdata[m][3] = sigma ;
  }

}

void loopT()
{

double Amin=0.0, Amax=2.0;
double mmin=.1, mmax=.9;
double Emin=80.0, Emax=90.0;
double Smin=130.0, Smax=150.0;
double Vmin=12, Vmax=15;
double Wmin=34.0, Wmax=40.0;

int seed = 100000 ;

for(int i = 0; i <= seed; i++){
	double rand_A = randfrom(Amin, Amax);
	double rand_m = randfrom(mmin, mmax);
	double rand_E = randfrom(Emin, Emax);
	double rand_S = randfrom(Smin, Smax);
	double rand_V = randfrom(Vmin, Vmax);
	double rand_W = randfrom(Wmin, Wmax);
	   
	likelihood(rand_A, rand_m, rand_E, rand_S, rand_V, rand_W);
	}
}


void likelihood(double  A, double m, double E, double S, double V, double W)
{ 
double D, tempo, lh, sigma;
double K, square_wave;
double sn, cn, dn, u;
double k = sqrt(m); //note the sqrt: m=k^2
double PHI = M_PI/2;
double c_x = 0.0;
double c_y = 0.0;
long int N = 100000000;
int j= 0;
int f = 0;
int g = 0;
int h = 0;
double index;
int s, p;
int it = 0;
int kt = 0;
int rt = 0;
lh = 0.0;
double *x = malloc( N * sizeof(double));
for(int n=1; n<=W;n++){
	/*This routine compute the incomplete elliptic integral F(phi,k)*/
	K = gsl_sf_ellint_F(PHI, k, 2);	
	for(u=-2.0*K*S/E;u<=2.0*K;u+=.01){
		/*This function computes the Jacobian elliptic functions sn(u|m), cn(u|m), dn(u|m) by descending Landen transformations. */
		gsl_sf_elljac_e(u, m, &sn, &cn, &dn);
		/*Square wave*/
		square_wave = step(u) - step(u-2*K);
		/*Coordenates*/
		c_x = E*u/(2*K) + (E + S)*W;
		c_y = square_wave*sn*A + V + x[j++];
		matriz[kt++][0] = c_x;
		matriz[rt++][1] = c_y;
		it++;
	}		
}	
	s = it;
	
	if(s > lines_input){
	index =	s / lines_input;
	} else {
	index = lines_input / s ;
	}

	//r = s/(int)index + 1;
	for(int nm = 0; nm<s; nm +=(int)index){
		nueva_matriz[f++][1] = matriz[nm][1];	
		nueva_matriz[g++][0] = matriz[nm][0];
h++;	
	}
p = h;
	
	for(int t = 0; t < p; t++){
		sigma = matrixdata[t][3];
		if (matriz[t][1] != 0){ 
		D = fabs( ( matrixdata[t][2] / nueva_matriz[t][1] ) - 1.0  ) ;
		
		if ( ( matrixdata[t][2] / nueva_matriz[t][1]) > 1.0 )
		{
		sigma = 2.0 * sigma ;
		}
		if(sigma != 0){
		tempo =  - ( D * D / ( 2.0 * sigma * sigma ) ) ;
		lh = lh + tempo ;
		}

	}
	}
	free (x);
fprintf(datafilewrite,"\n%f\t%f\t%f\t%f\t%f\t%f\t%f", lh, A, m, E, S, V, W);
}


double step(double x)
{
	if(x>=0)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

void openfiles()
{

//Open datafilewrite:
  datafilewrite = fopen("output.dat", "w");

  datafileread = fopen("mrk501_optical_clean.dat", "r");

  if (datafilewrite == NULL )
    {
     (void)printf("The data file output-prueba.dat was not OPEN \n\r"); 
    }
  if (datafileread == NULL )
    {
     printf("The data file observationaldata.dat was not OPEN \n\r");
    }

}

void closefiles()
{

  fclose(datafilewrite);
  fclose(datafileread);

}

double numero;
/* generate a random floating point number from min to max */
double randfrom(double min, double max) 
{
double r;
double range = max - min;
double buckets = RAND_MAX / range;
double limit = buckets * range;

    do {
        r = rand();
      
    } while (r >= limit);

    return min + (r / buckets);

}

