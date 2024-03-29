## Tunisian Arabish Corpus (TArC)

This repository describes and contains the corpus mentioned in the following papers: 

* [Gugliotta, E. & Dinarelli, M. (2020, May). TArC: Incrementally and Semi-Automatically Collecting a Tunisian Arabish Corpus. In Proceedings of The 12th LREC (pp. 6279-6286).](https://www.aclweb.org/anthology/2020.lrec-1.770/)
* [Gugliotta, E., & Dinarelli, M. (2020, June). TArC. Un corpus d'arabish tunisien. In Actes: JEP-TALN (RÉCITAL).Vol 2: (pp. 232-240). ATALA.](https://hal.archives-ouvertes.fr/hal-02784772/)
* [Gugliotta, E. et al., (2020). Multi-Task Sequence Prediction For Tunisian Arabizi Multi-Level Annotation.](https://www.aclweb.org/anthology/2020.wanlp-1.16/)

TArC has been designed as a flexible and multi-purpose open corpus in order to be a useful support for different types of analyses: computational and linguistics, as well as for NLP tools training. 

Arabish, also known as *Arabizi*, is a spontaneous encoding of Arabic dialects in Latin characters and *arithmographs* (numbers used as letters). This **code-system** was developed by Arabic-speaking users of social media in order to facilitate the writing in the Computer Mediated Communication (CMC) and text messaging informal frameworks [[2]](#2).

<!-- - TArC is thus the result of a multidisciplinary work with a hybrid approach based on : 
* dialectological research questions 
* corpus linguistic criteria 
  * Text mode: informal writing 
  * Text *genre*: social media (forums, blogs, social network, rap lyric) 
  * Domain: CMC
  * Language: Tunisian encoded in Arabish
  * Location & Publication date: extracted together with the texts metadata
* deep learning techniques  -->

### *Overview of TArC*

In a nutshell, the data gathered in TArC represent **Tunisian Arabish writing and its evolution over the last ten years**.   

TArC texts have been  extracted from social media for an amount of 43 313 tokens. Each text has been extracted together with the user's **metadata** when publicly shared. 
The metadata consists in: 
* **The governorate of provenance**
* **Age range**: [-25],[25-35],[35-50],[50+]
* **Gender**: M/F 

The Tunisian Arabish texts collected in the TArC have been provided with various annotation levels semi-automatically produced by a [Multi-Task Sequence Prediction System](https://gricad-gitlab.univ-grenoble-alpes.fr/dinarelm/tarc-multi-task-system): 

* Token classification into *arabizi*, *foreign* and *emotag*. 
* Encoding in Arabic Script of the tokens classified as *arabizi* (following the CODA convention [[4]](#4)).
* Tokenization of the *CODAfied* texts.
* Part-of-Speech tagging for the *arabizi* tokens.

TArC numbers:

|               |**SENTENCES**|         |**WORDS**|         |
|:--------------|:-----------:|:-------:|:-------:|:-------:|
|**TOTAL**      |   4,797     |         |  43,327 |         |
|               |             |*arabizi*|*foreign*|*emotag* |
|Forum (11,909) | 755         |6,024    |5,873    |12       |
|Social (16,056)| 3,162       |11,835   |3,623    |598      |
|Blog (6,671)   | 366         |5,970    |694      |7        |
|Rap (8,691)    | 514         |7,681    |1,009    |1        |

<br />

### *Classification* 
<!-- classificationRepositiryWhenThereWillBeOne -->
The classification task consists in categorizing the text at the token level into three classes: *arabizi*, *foreign* and *emotag*. The first class is for Tunisian and Modern Standard Arabic tokens; the second one is used to classify non-Arabic code-mixing or code-switching elements; the latter is the label used for elements such as smiley or emoticons. This operation is preparatory to the second level of annotation, aka the *encoding in Arabic characters*.

The token-level classification has been carried on through a RNN character-level model pre-trained on: 
1.    [Hussem Ben Belgacem's French dictionary](https://github.com/hbenbel/French-Dictionary), consisting in 336 351 tokens
2.    A Tunisian Arabish dictionary of 100 936 tokens, resulting from the merge of the following datasets: 
* [The Tunizi Sentiment Analysis Tunisian Arabic Dataset](https://github.com/chaymafourati/TUNIZI-Sentiment-Analysis-Tunisian-Arabizi-Dataset) [[1]](#1)  
* The TLD dataset of Arabish [[6]](#6)

The *emotag* dictionary was built by extracting smileys and emoticons from the Arabizi dictionary (2nd item).
Once the model was pre-trained on the above data, it has been possible to start an iterative procedure for TArC text classification. [[3]](#3) The model reached 97% of accuracy.   
Each token classification has been manually checked. 


<br />

### *Tokenization and PoS tagging*
The tokenization at string level consists in reducing each string to its components, concatenated by the symbol +. Only those tokens classified as *arabizi* have been tokenized.
<br />
E.g.: "be in a bad lay" (lit.:*on the wall*), [ʕal'ħiːtˤ], ع+ال+حيط <= عالحيط

The Part-of-Speech tagging is the morphosyntatic annotation of strings. It has been operated at both levels: morphological and functional. The first one describes the morphological nature of each element of the string, while the second one describes the grammatical function of the whole string. 
The PoS annotation style follows the guidelines of the *Penn Arabic Treebank* (PATB) [[5]](#5). 

| *arabish* | *CODA* | *tokenization* | *POS*                    |*gloss*|
|:---------:|:------:|:--------------:|:------------------------:|:----:|
| sa7a	    |	صحّة      |  صحّة       |[NOUN-NSUFF_FEM_SG]INTERJ | lit:health |
| w	        |	و    |    و           |CONJ                      | and    |
| bechfee	|بالشفى |ب+ال+شفى         |[PREP+DET+NOUN]INTERJ     |  lit:to your good health |

<br />

### *How to use TArC*

It is possible to download TArC text files organized by genres: 

* Forum texts: *forum.tab*
* Social Network texts: *social.tab*
* Blog texts: *blog.tab* 
* Rap lyrics texts: *rap.tab* 


In each file, the sentences are delimited by a blank line and each file contains the header such as: 


|data|arabish|class|coda|token|pos|governorate|age|
|:--:|:-----:|:--:|:---:|:---:|:-:|:--:|:-:|

\
The publication date information follow the structure: yyyymmdd. 

Not all sentences are provided with all the metadata information (governorate/age/gender). You can find '/' in place of the metadata, it means that the users didn't published this information. 

The governorate names are encoded following the French orhographical conventions and are: 
*Ariana, Béja, Sousse, Bizerte, Gabès, Nabeul, Jendouba, Kairouan, Zaghouan, Kebili, El Kef, Mahdia, Manouba, Medenine, Monastir, Gafsa, Sfax, Sidi Bouzid, Siliana, Ben Arous, Tataouine, Tozeur, Tunis, Kasserine*. 

Any user personal information has been anonymized by covering it with the token: 

*m5abbi+id number*

The Tunisian word 'm5abbi' means 'covered', correspond to the *CODAfied* token 'مخبّي' and the PoS-tag: 'NOUN_PROP'.  

If you want to use this data with the [Multi-Task Sequence Prediction System](https://gricad-gitlab.univ-grenoble-alpes.fr/dinarelm/tarc-multi-task-system), you should remove the header and extract the columns that you need, depending on process that you want to perform. 

The lemmatization layer is coming, as is a distribution of the data in Excel format.

<br />

### *License*

Attribution 4.0 International (CC BY-NC-SA 4.0) 

<br />

### *Citation* 

Please cite this work as: 

````bibtex
@inproceedings{gugliotta-etal-wanlp2020, 
    title={Multi-Task Sequence Prediction For Tunisian Arabizi Multi-Level Annotation}, 
    author={Gugliotta, Elisa and Dinarelli, Marco and Kraif, Olivier}, 
    booktitle={The Fifth Arabic Natural Language Processing Workshop (WANLP)}, 
    year={2020},
}

````


<br />

## References 

<a id="1">[1]<a/>
Fourati, C. et al., (2020). TUNIZI: a Tunisian Arabizi sentiment analysis Dataset. *arXiv preprint arXiv:2004.14303*.

<a id="2">[2]<a/>
Gugliotta, E. & Dinarelli, M. (2020, May). TArC: Incrementally and Semi-Automatically Collecting a Tunisian Arabish Corpus. *In Proceedings of The 12th Language Resources and Evaluation Conference (pp. 6279-6286)*.

<a id="3">[3]<a/>
Gugliotta, E. et al., (2020). Multi-Task Sequence Prediction For Tunisian Arabizi Multi-Level Annotation. Accepted for *The Fifth Arabic Natural Language Processing Workshop (WANLP) 2020. Forthcoming*. 

<a id="4">[4]<a/>
Habash, N. et al., (2012, May). Conventional Orthography for Dialectal Arabic. *In Proceedings of The Language Resources and Evaluation Conference (pp. 711-718)*.

<a id="5">[5]<a/>
Maamouri, M. et al., (2009). *Penn Arabic Treebank guidelines v4.*

<a id="6">[6]<a/>
Younes, J., et al., (2015, June). Constructing linguistic resources for the Tunisian dialect using textual user-generated contents on the social web. *In International Conference on Web Engineering (pp. 3-14)*. Springer, Cham.