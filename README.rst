|Python Version| |Version| |License|

KaMI-lib (Kraken Model Inspector)
=================================

|Logo|

HTR / OCR models evaluation agnostic Python package, originally based on
the `Kraken <http://kraken.re/>`__ transcription system.

🔌 Installation
===============

User installation
-----------------

Use pip to install package:

.. code-block:: bash

    $ pip install kamilib

Developer installation
----------------------

1. Create a local branch of the kami-lib project

.. code-block:: bash

    $ git clone https://gitlab.inria.fr/dh-projects/kami/kami-lib.git

2. Create a virtual environment

.. code-block:: bash

    $ virtualenv -p python3.7 kami_venv

then

.. code-block:: bash

    $ source kami_venv/bin/activate

3. Install dependencies with the requirements file

.. code-block:: bash

    $ pip install -r requirements.txt

4. Run the tests

.. code-block:: bash

    $ python -m unittest tests/*.py -v

🏃 Tutorial
===========

An "end-to-end pipeline" example that uses Kamilib (written in French)
is available at: |Open In Colab|

Tools build with KaMI-lib
-------------------------

A turn-key graphical interface :
`KaMI-app <https://kami-app.herokuapp.com/>`__

🔑 Quickstart
==============

KaMI-lib can be used for different use cases with the class `Kami()`.

First, import the KaMI-lib package :

.. code-block:: python

    from kami.Kami import Kami

The following sections describe two use cases :

-  How to compare outputs from any automatic transcription system,
-  How to use KaMI-lib with a transcription prediction produced with a
   Kraken model.

Summary
-------

1. Compare a reference and a prediction, independently from the Kraken engine
2. Evaluate the prediction of a model generated with the Kraken engine
3. Use text preprocessing to get different scores
4. Metrics options
5. Others

1. Compare a reference and a prediction, independently from the Kraken engine
-----------------------------------------------------------------------------

KaMI-lib allows you to compare two strings or two text files by
accessing them with their path.

.. code-block:: python

    # Define your string to compare.
    reference_string = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."

    prediction_string = "Les 14a de Maxime ! étaient, djàteriblement, savants - La Curée, 1871. En avant? pour la leTTture."

    # Or specify the path to your text files.
    # reference_path = "reference.txt"
    # prediction_path = "prediction.txt"

    # Create a Kami() object and simply insert your data (string or raw text files)
    k = Kami([reference_string, prediction_string]) 

you can retrieve the results as dict with the `.board` attribute:

.. code-block:: python

    print(k.scores.board)

which returns a dictionary containing your metrics (see also Focus on
metrics section further):

.. code-block:: python

    {'levensthein_distance_char': 14, 'levensthein_distance_words': 8, 'hamming_distance': 'Ø', 'wer': 0.4, 'cer': 0.13333333333333333, 'wacc': 0.6, 'wer_hunt': 0.325, 'mer': 0.1320754716981132, 'cil': 0.17745383867832842, 'cip': 0.8225461613216716, 'hits': 92, 'substitutions': 5, 'deletions': 8, 'insertions': 1}

You can also access a specific metric, as follows:

.. code-block:: python

    print(k.scores.wer)

2. Evaluate the prediction of a model generated with the Kraken engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `Kami()` object uses a ground truth (**XML ALTO or XML PAGE format
only, no text format**), a transcription model and an image to evaluate
prediction made by the Kraken engine.

Here is a simple example demonstrating how to use this method with a
ground truth in ALTO XML:

.. code-block:: python

    # Define ground truth path (XML ALTO here)
    alto_gt = "./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_alto.xml"
    # Define transcription model path
    model="./datatest/lectaurep_set/models/mixte_mrs_15.mlmodel"
    # Define image
    image="./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0.png"

    # Create a Kami() object and simply insert your data
    k = Kami(alto_gt,
             model=model,
             image=image)  

To retrieve the results as dict (`.board` attribute), as use case 1.:

.. code-block:: python

    print(k.scores.board)

which returns a dictionary containing your metrics (for more details on
metrics see section ...):

.. code-block:: python

    {'levensthein_distance_char': 408, 'levensthein_distance_words': 255, 'hamming_distance': 'Ø', 'wer': 0.3128834355828221, 'cer': 0.09150033639829558, 'wacc': 0.6871165644171779, 'wer_hunt': 0.29938650306748466, 'mer': 0.08970976253298153, 'cil': 0.1395071670835435, 'cip': 0.8604928329164565, 'hits': 4140, 'substitutions': 238, 'deletions': 81, 'insertions': 89}

Depending on the size of the ground truth file, the prediction process
may take more or less time.

Kraken parameters can be modified. You can specify the number of CPU
workers for inference (default 7) with the ``workers`` parameter and you
can set the principal text direction with the ``text_direction``
parameter ("horizontal-lr", "horizontal-rl", "vertical-lr ",
"vertical-rl". By default Kami uses "horizontal-lr".).

.. code-block:: python

    k = Kami(alto_gt,
             model=model,
             image=image,
             workers=7,
             text_direction="horizontal-lr")  

3. Use text preprocessing to get different scores
-------------------------------------------------

KaMI-lib provides the possibility to apply textual transformations on
the ground truth and the prediction before evaluating them. By doing so,
scores can change according to the performance of the model used. This
functionality allows a better made by the transcription model. For
example, if removing all diacritics improves the scores, it probably
means that the model is not good enough at transcribing them. By default
no preprocessing is applied.

To preprocess the ground truth and the prediction, you can use `apply_transforms` parameter from `Kami()` class.

The `apply_transforms` parameter receives a character code
corresponding to the transformations to be performed :

+------------------+----------------------------------------------------------------------------+
| Character code   | Applied transformation                                                     |
+==================+============================================================================+
| D                | remove digits                                                              |
+------------------+----------------------------------------------------------------------------+
| U                | uppercase                                                                  |
+------------------+----------------------------------------------------------------------------+
| L                | lowercase                                                                  |
+------------------+----------------------------------------------------------------------------+
| P                | remove punctuation                                                         |
+------------------+----------------------------------------------------------------------------+
| X                | remove diacritics                                                          |
+------------------+----------------------------------------------------------------------------+

You can combine these options as follows:

.. code-block:: python

    k = Kami(
        [ground_truth, prediction],
        apply_transforms="XP" # Combine here : remove diacritics + remove punctuation  
        )  

It results in a dictionary of more complex scores (use built-in
``pprint`` module to create a human readable dict.), as follows:

.. code-block:: python

    import pprint

    # Get all scores
    pprint.pprint(k.scores.board)

.. code-block:: python

    {'Length_prediction': 2507,
          'Length_prediction_transformed': 2405,
          'Length_reference': 2536,
          'Length_reference_transformed': 2426,
          'Total_char_removed_from_prediction': 102,
          'Total_char_removed_from_reference': 110,
          'Total_diacritics_removed_from_prediction': 84,
          'Total_diacritics_removed_from_reference': 98,
          'all_transforms': {'cer': 5.81,
                             'cil': 8.38,
                             'cip': 91.61,
                             'deletions': 48,
                             'hamming_distance': 'Ø',
                             'hits': 2312,
                             'insertions': 27,
                             'levensthein_distance_char': 141,
                             'levensthein_distance_words': 73,
                             'mer': 5.74,
                             'substitutions': 66,
                             'wacc': 82.28,
                             'wer': 17.71},
          'default': {'cer': 6.62,
                      'cil': 9.55,
                      'cip': 90.44,
                      'deletions': 59,
                      'hamming_distance': 'Ø',
                      'hits': 2398,
                      'insertions': 30,
                      'levensthein_distance_char': 168,
                      'levensthein_distance_words': 90,
                      'mer': 6.54,
                      'substitutions': 79,
                      'wacc': 79.54,
                      'wer': 20.45},
          'remove_diacritics': {'cer': 6.08,
                                'cil': 8.78,
                                'cip': 91.21,
                                'deletions': 49,
                                'hamming_distance': 'Ø',
                                'hits': 2379,
                                'insertions': 31,
                                'levensthein_distance_char': 152,
                                'levensthein_distance_words': 77,
                                'mer': 6.0,
                                'substitutions': 72,
                                'wacc': 82.05,
                                'wer': 17.94},
          'remove_punctuation': {'cer': 6.37,
                                 'cil': 9.25,
                                 'cip': 90.74,
                                 'deletions': 57,
                                 'hamming_distance': 'Ø',
                                 'hits': 2330,
                                 'insertions': 25,
                                 'levensthein_distance_char': 157,
                                 'levensthein_distance_words': 86,
                                 'mer': 6.31,
                                 'substitutions': 75,
                                 'wacc': 79.71,
                                 'wer': 20.28}}

-  The **'default'** key indicates the scores without any
   transformations;
-  The **'all\_transforms'** key indicates the scores with all
   transformations applied (here remove diacritics + remove
   punctuation).

If you have used text preprocessing, for example:

-  The **'remove\_punctuation'** key indicates the scores with removed
   punctuations only;
-  The **'remove\_diacritics'** key indicates the scores with removed
   diacritics only.

4. Metrics options
------------------

KaMI provides the possibility to weight differently the operations made
between the ground truth and the prediction (as insertions,
substitutions or deletions). By default this operations have a weight of
1. You can change these weigthts with the parameters in the `Kami()`
class:

-  `insertion_cost`
-  `substitution_cost`
-  `deletion_cost`

**Keep in mind that these weights are the basis for Levensthein distance
computations and performance metrics like WER and CER, which can greatly
influence final scores.**

Example:

.. code-block:: python

    k = Kami(
        [ground_truth, prediction],
        insertion_cost=1,
        substitution_cost=0.5,
        deletion_cost=1
        )  

`Kami()` class also provides score display settings :

-  `truncate` (bool) : Option to truncate result. Defaults to
   `False`.
-  `percent` (bool) : `True` if the user want to show result in
   percent else `False`. Defaults to `False`.
-  `round_digits` (str) : Set the number of digits after floating
   point in string form. Defaults to `'.01'`.

Example :

.. code-block:: python

    k = Kami([ground_truth, prediction],
                 apply_transforms="DUP", 
                 verbosity=False,  
                 truncate=True,  
                 percent=True,  
                 round_digits='0.01')  

5. Others
---------

For debugging you can pass the `verbosity` (defaults to `False`)
parameter in the `Kami()` class, this displays execution logs.

🎯 Focus on metrics
===================

Operations between strings
--------------------------

-  **Hits**: number of identical characters between the reference and
   the prediction.

-  **Substitutions**: number of substitutions (a character replaced by
   another) necessary to make the prediction match the reference.

-  **Deletions**: number of deletions (a character is removed) necessary
   to make the prediction match the reference.

-  **Insertions**: number of insertions (a character is added) necessary
   to make the prediction match the reference.

*for each of these operations, except hits, a cost of 1 is assigned by
default.*

Distances
---------

-  **Levensthein Distance (Char.)**: Levenshtein distance (sum of
   operations between character strings) at character level.

-  **Levensthein Distance (Words)**: Levenshtein distance (sum of
   operations between character strings) at word level.

-  **Hamming Distance**: A score if the strings' lengths match but their
   content is different; `Ø` if the strings' lengths don't
   match.

Transcription performance (HTR/OCR)
-----------------------------------

The performance metrics are calculated with the Levenshtein distances
mentioned above.

-  **WER** : Word Error Rate, proportion of words bearing at least one recognition error. 
   It is generally between `[0, 1.0]`, the closer it is to `0` the better the recognition. 
   However, a bad recognition can lead to a `WER> 1.0`.

-  **CER** : Character Error Rate, proportion of characters erroneously transcribed. 
   Generally more accurate than WER. It is generally between `[0, 1.0]`, the closer it is to
   `0` the better the recognition. However, a bad recognition can lead to a `CER> 1.0`.

-  **Wacc** : Word Accuracy, proportion of words bearing no recognition error.

-  **WER Hunt** : reproduce the Word Error Rate experiment by Hunt (1990). 
   Same principle as WER computation with a weighting of `O.5` on insertions and deletions. 
   This metric shows the importance of customizing the weighting of operations made between strings as it depends heavily on the system 
   and type of data used in an HTR/OCR project. In KaMI-lib, it is possible to modify the weigthts assigned to operations.

Experimental Metrics (metrics borrowed from Speech Recognition - ASR)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Match Error Rate**

-  **Character Information Lost**

-  **Character Information Preserve**

❓ Do you have questions, bug report, features request or feedback ?
====================================================================

Please use the issue templates:


- 🐞 Bug report: `here <https://github.com/KaMI-tools-project/KaMi-lib/issues/new?assignees=&labels=&template=bug_report.md&title=>`__


- 🎆 Features request: `here <https://github.com/KaMI-tools-project/KaMi-lib/issues/new?assignees=&labels=&template=feature_request.md&title=>`__

*if aforementioned cases does not apply, feel free to open an issue.*

✒️ How to cite
==============

.. code-block:: latex

    @misc{Kami-lib,
        author = "Lucas Terriel (Inria - ALMAnaCH) and Alix Chagué (Inria - ALMAnaCH)",
        title = {Kami-lib - Kraken model inspector},
        howpublished = {\url{https://github.com/KaMI-tools-project/KaMi-lib}},
        year = {2021-2022}
    }

🐙  License and contact
=======================

Distributed under `MIT <./LICENSE>`__ license. The dependencies used in
the project are also distributed under compatible license.

Mail authors and contact: Alix Chagué (alix.chague@inria.fr) and Lucas
Terriel (lucas.terriel@inria.fr)

Special thanks: Hugo Scheithauer (hugo.scheithauer@inria.fr)

*KaMI-lib* is developed and maintained by authors (2021-2022, first
version named Kraken-Benchmark in 2020) with contributions of
`ALMAnaCH <http://almanach.inria.fr/index-en.html>`__ at
`Inria <https://www.inria.fr/en>`__ Paris.

|forthebadge made-with-python|

.. |Logo| image:: https://raw.githubusercontent.com/KaMI-tools-project/KaMi-lib/master/docs/static/kamilib_logo.png
    :width: 100px
.. |Python Version| image:: https://img.shields.io/badge/Python-%3E%3D%203.7-%2313aab7
   :target: https://img.shields.io/badge/Python-%3E%3D%203.7-%2313aab7
.. |Version| image:: https://badge.fury.io/py/kamilib.svg
   :target: https://badge.fury.io/py/kamilib
.. |License| image:: https://img.shields.io/github/license/Naereen/StrapDown.js.svg
   :target: https://opensource.org/licenses/MIT
.. |Open In Colab| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/drive/1nk0hNtL9QTO5jczK0RPEv9zF3nP3DpOc?usp=sharing
.. |forthebadge made-with-python| image:: http://ForTheBadge.com/images/badges/made-with-python.svg
   :target: https://www.python.org/

