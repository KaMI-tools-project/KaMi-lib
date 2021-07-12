from kami.metrics._base_metrics import _hot_encode
import Levenshtein



#####################################
### SUB-SYSTEMS CLASS OF KAMI LIB ###
#####################################

## >> Private or abstract class or functions : Preprocessing


## >> Public class

# Preprocessing Module #




class KamiScorer:
    def __init__(self, reference: str, prediction: str):
        self.reference = reference
        self.prediction = prediction
        self.lev_char_level = self.levensthein_distance_char()
        self.lev_words_level = self.levensthein_distance_words()
        self.board = {
            "default": {
                "lev_words": self.lev_words_level
            }
        }


    def levensthein_distance_char(self):
        """Compute Levensthein distance from C extension module Python-Levensthein."""
        # Compute levensthein at char level
        lev_distance_char = Levenshtein.distance(self.reference, self.prediction)
        return lev_distance_char

    def levensthein_distance_words(self):
        """Compute Levensthein distance from C extension module Python-Levensthein."""
        # Compute levensthein at word level
        lev_distance_words = Levenshtein.distance(*_hot_encode(
            [self.reference.split(), self.prediction.split()]))
        return lev_distance_words


