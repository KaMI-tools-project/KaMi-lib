#include <stdio.h>
#include <stdlib.h>
#include "metrics_lib.h"

/* HTR OCR metrics functions */

float WordErrorRate(int lev_distance_word, int total_reference_word)
{
    return (float)lev_distance_word / (float)total_reference_word;
};

float CharacterErrorRate(int lev_distance_char, int total_reference_char)
{
    return (float)lev_distance_char / (float)total_reference_char;
};

float WordErrorRateHuntStyle(float total_w, float total_reference_word)
{
    return total_w/total_reference_word;
};

float WordAccuracy(float wer)
{
    return (1.0 - wer);
};

/* ASR metrics functions */

float CharacterInformationPreserve(int hits, int total_reference_char, int total_prediction_char)
{
    float h = (float)hits;
    return (h/(float)total_reference_char)*(h/(float)total_prediction_char);
};

float CharacterInformationLost(float cip)
{
    return (1.0 - cip);
};

float MatchErrorRate(int hits, int lev_distance_char)
{
    return (float)lev_distance_char/((float)hits+(float)lev_distance_char);
};
