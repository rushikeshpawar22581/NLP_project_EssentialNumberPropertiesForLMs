# NLP_project
**Defining and Testing Essential Number Properties for LMs**

Students:
1. Karan Raj Bagri              (karanraj@iisc.ac.in)
2. Dhamale Vivek Shrikrishna    (viveksd@iisc.ac.in)
3. Pawar Rushikesh Gajanansa    (rushikeshp@iisc.ac.in)

Abstract:
Language Models have achieved impressive feats in Natural Language Processing, 
excelling at tasks like text generation, machine translation, Question Answers, 
text summarization. However, NLP systems rarely give special considerations to numbers. 
They are treated just like any other text tokens, but there is a fundamental 
difference between words/letters and numbers. Also, during preprocessing most of the numbers get mapped to
<UNK> token because of absence from the vocabulary. This results in
poor number play despite great wordplay that these models can perform.
In this project, we intend to come up with a set of properties that LMs
should know about numbers, and we will try to build tests to check how
much numeracy is captured by current models.
