# NLP/Naive Bayes Project

## Objective: 
To classify user comments about some products into "Recommending" and "Non-Recommending" comments, using Naive Bayes classifier. 

## Implementation: 
All of the implementation methods are aptly discussed in the [Python Code](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3_code.py), [Jupyter Notebook File](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3.ipynb) and [HTML File](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3_Report.html), but briefly explaining, our dataset included a number of users' comments' titles and text on the products sold on "DigiKala" platform, the most popular Iranian online shop. By applying the "Bag of Words" technique to the comments in the training dataset, we designed a classifier to recognize "Recommending" comments in the test dataset. For this purpose, the odds of each word's appearance in both classes were calculated. Consequently, the conditional probability of a comment being "Recommending" or "Non-Recommending" was computable using Naive Bayes formula. The classifier's judgment is the label with a higher probability.  
Notably, applying pre-processing methods to our dataset was necessary. Hence, appropriate pre-processing methods were tested, and their results were analyzed. The Additive Smoothing technique was used to avoid reaching the probability of 0 in case of seeing new words in the test dataset, which enhanced the precision of our model significantly.  
Finally, some falsely classified comments were analyzed to identify the flaws of our model.

## Results: 
All of the results are aptly discussed in the [Jupyter Notebook File](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3.ipynb) and [HTML File](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/CA3_Report.html), but the table below shows the average performance of our Naive Baise model at a glance.

![alt text](https://github.com/moeinsh78/Artificial-Intelligence-Course-Projects/blob/master/NLP-NB/table.JPG)
