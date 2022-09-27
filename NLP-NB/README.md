# Artificial-Intelligence-Course-Projects

## Objective: 
To classify user comments about some products to "Recommending" and "Non-Recommending" comments, using Naive Bayes classifier. 

## Implementation: 
All of the implementation methods are aptly discussed in the [Python Code](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3_code.py), [Jupyter Notebook File](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3.ipynb) and [HTML File](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3_Report.html), but briefly explaining, our dataset included a number of user's comments title and text on the products sold on "DigiKala" platform, the most popular Iranian online shop. By appliying the "Bag of Words" technique on the comments in train dataset, we designed a classifier to recognize "Recommending" comments in the test dataset. For this purpose, the odds of each word's appearance in both classes were calculated. Consequently, the conditional probability of a comment being "Recommending" or "Non-Recommending" was computable using Naive Bayes formula. The classifier's judgement is the label with a higher probability.  
It is notable that applying pre-processing methods on our dataset was necessary. Hence, appropriate pre-processing methods were tested and their results were analyzed.  
Finally, some falsely classified comments were analyzed to identify the flaws of our model.

## Results: 
All of the results are aptly discussed in the [Jupyter Notebook File](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3.ipynb) and [HTML File](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3_Report.html), but the table below shows the overage performance of our Naive Baise model in a glance.

![alt text](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/table.JPG)
