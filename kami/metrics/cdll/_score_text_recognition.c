// #include "_distance.c"

/***************************************************************************************

            C SUB-LIBRARY FOR TEXT RECOGNITION METRICS (CDLL)
            ================================================

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

            $ gcc -Wall _score_text_recognition.c -o distance -lm

3) Test :

            $ ./distance

4) if all are ok, create .so file with (change warning compiler level) :

            $ cc -fPIC -Wextra -shared -o .././so_extensions/_score_text_recognition.so _score_text_recognition.c

******************************************************************************************/

/*
sub-functions
-------------

- countWords() : returns number of words in string
- countChar() : returns number of characters in string
*/
/*
#define OUT    0
#define IN     1

unsigned countWords(wchar_t *str) {
    int state = OUT;
    unsigned wc = 0;  // word count

    // Scan all characters one by one
    while (*str)
    {
        // If next character is a separator, set the
        // state as OUT
        if (*str == ' ' || *str == '\n' || *str == '\t')
            state = OUT;

        // If next character is not a word separator and
        // state is OUT, then set the state as IN and
        // increment word count
        else if (state == OUT)
        {
            state = IN;
            ++wc;
        }

        // Move to next character
        ++str;
    }

    return wc;
}

unsigned countChar(wchar_t *str) {

    unsigned cc = 0;  // char count

    // Scan all characters one by one
    while (*str)
    {
        ++cc;
        // Move to next character
        ++str;
    }

    return cc;

}
*/

/*
main recognition metrics functions
---------------------------------

1 - Word Error Rate (WER)
2 - Character Error Rate (CER)
3 - Word accuracy (Wacc)

*/

/********************************/

float wer(int total_words_reference, int lev_dist) {
     return (float) lev_dist/total_words_reference;

}

/********************************/

float cer(int total_char_reference, int lev_dist) {
     return (float) lev_dist/total_char_reference;

}

/********************************/

float wacc(int total_words_reference, int lev_dist) {
    return (float) (1 - wer(total_words_reference, lev_dist));
}

/*
int main()
{
    float result_wer, result_cer, result_wacc;
    int lev;
    int wc, cc;
    int lev_distance = 10;

    wchar_t ref[] = L"Bonjour le peuple du monde de la terre bleue",

    target[] = L"Bjour le puple du Monde de la terre bleue";

    wc = countWords(ref);
    cc = countChar(ref);

    result_wer = WER(ref, target);
    result_cer = CER(ref, target);
    result_wacc = Wacc(ref, target);
    lev = levenshtein(ref, target);
    printf("WER : %f\n", result_wer);
    printf("CER : %f\n", result_cer);
    printf("Wacc : %f\n", result_wacc);
    printf("Lev : %i\n", lev);
    printf("Total words in ref : %i\n", wc);
    printf("Total char in ref : %i\n", cc);

    return 0;
}
*/