#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

/***************************************************************************************

            C SUB-LIBRARY FOR DISTANCE METRICS (CDLL)
            ========================================

# Author : Lucas Terriel <lucas.terriel@inria.fr>
# Last release : 04/02/2021
# Licence : MIT

                      ==================
                             NOTE
                      ==================

If change this script, ensure :

1) Write a test the call direcly in the call or in comment
main() function
2) Compile C program with :

            $ gcc -Wall _distance.c -o distance -lm

3) Test :

            $ ./distance

4) if all are ok, create .so file with (change warning compiler level) :

            $ cc -fPIC -Wextra -shared -o .././so_extensions/_distance.so _distance.c

******************************************************************************************/


/*
sub-functions
-------------

- min() : returns the minimum between three values
*/

int min(int a, int b, int c){
	if(a <= b && a <= c){
		return a;
	}
	else if(b <= a && b <= c){
		return b;
	}
	else if(c <= a && c <= b){
		return c;
	}
	return(0);
}

/*
main distance functions
-----------------------

1 - Levenshtein distance (edit distance)
2 - Hamming distance

*/

/********************************/

int levenshtein(wchar_t *s1, wchar_t *s2) {
    // Uncomment to test the unicode (wchar_t not char) passing string bellow :
    // printf("Ma sequence 1 en C : %ls\n", s1);
    // printf("Ma sequence 2 en C : %ls\n", s2);
    unsigned int x, y, s1len, s2len;
    // strlen() use for C type char, here use wcslen()
    s1len = wcslen(s1);
    s2len = wcslen(s2);
    unsigned int matrix[s2len+1][s1len+1];
    matrix[0][0] = 0;
    for (x = 1; x <= s2len; x++)
        matrix[x][0] = matrix[x-1][0] + 1;
    for (y = 1; y <= s1len; y++)
        matrix[0][y] = matrix[0][y-1] + 1;
    for (x = 1; x <= s2len; x++)
        for (y = 1; y <= s1len; y++)
            matrix[x][y] = min(matrix[x-1][y] + 1, matrix[x][y-1] + 1, matrix[x-1][y-1] + (s1[y-1] == s2[x-1] ? 0 : 1));

    return(matrix[s2len][s1len]);
}

/********************************/

int hamming(wchar_t str1[], wchar_t str2[])
{
    int i = 0, count = 0;
    while(str1[i]!='\0')
    {
        if (str1[i] != str2[i])
            count++;
        i++;
    }
    return count;
}

/********************************/

/*
int main()
{
    wchar_t ref[] = L"Ne vous défiez jamais de votre voisin de gauche qui a une chemise de grosse toile, une cravate blanche, un habit propre,",

    target[] = L"Ne vous défiez jamais de votre vopsin de gopche qui a une chemise de grosse toile, une cravate blanche, an habit propre,";
    int result;

    result = hamming(ref, target);
    printf("%i\n", result);

    return result;
}
*/