float WordErrorRate(int lev_distance_word, int total_reference_word);
float CharacterErrorRate(int lev_distance_char, int total_reference_char);
float WordErrorRateHuntStyle(float total_w, float total_reference_word);
float WordAccuracy(float wer);
float CharacterInformationPreserve(int hits, int total_reference_char, int total_prediction_char);
float CharacterInformationLost(float cip);
float MatchErrorRate(int hits, int lev_distance_char);