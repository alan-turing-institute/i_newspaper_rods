To run the queries over the New Zealand Paper Past:
================================================================================

1. files.txt

D=/mnt/lustre/aroubick/PP_XMLs
for i in `ls $D`; do echo $D/$i; done > files.txt
mv files.txt ~/i_newspaper_rods/
================================================================================

2. queries

 .1 interesting gender words with context
 ========================================
    fab standalone.prepare:query=queries/article_xml_with_words-PP.py,datafile=query_args/interesting_gender_words-short.txt
    cd standalone
    spark-submit --py-files newsrods.zip newsrods/standalone_runner.py 144 > output_submission 

    -- this query often fails because it tries to return the whole article every time it finds an interesting word, and the list of words is quite long so the returned text runs out of memory 
    => run with less interesting words or words that will get less matches; or adjust output to be shorter (e.g., return only article's title)

 .2 interesting gender words (counts)
 ====================================
    fab standalone.prepare:query=queries/articles_countaining_words-PP.py,datafile=query_args/interesting_gender_words.txt
    cd standalone
    spark-submit --py-files newsrods.zip newsrods/standalone_runner.py 144 > output_submission

    -- this query runs fine

 .3 krakatoa/krakatua
 ====================
    fab standalone.prepare:query=queries/articles_containing_words-PP.py,datafile=query_args/interesting_words.txt
    cd standalone
    nohup spark-submit --py-files newsrods.zip newsrods/standalone_runner.py 144 > output_submission

   -- the query runs but the result is empty, there is no occurance of Krakatoa/tua in this set of articles (I have tested this by modifying one article by inserting the word Krakatoa in it and the query finds it, but it's the only one. When reverted to the original state, the archive doesn't contain neither of these words.
================================================================================

3. code
 
 The resulting files were changed in order to allow the archive to be queried:

 .1 issue.py
    Issue now corresponds to a generic set of articles, the articles have in common only the xml file they are coming from. The articles may or may not belong to the same edition or have been published on the same date. Therefore, the issue.py script loads only the minimal information --- it is root at <search> tag (which is the root of the xml structure) and creates one article object for every <result> found in the file. It seems that there are 100 articles in each xml file.
    -> removed date, page_count and day_of_week information

 .2 article.py
    Articles now need to track all the information that used to be recorded in an issue. The xml tags used in PaperPast archive differ from the BL ones, so there are further adjustments for that.
   
    -> text of the article is recorded as a string, not an array of words (hencethe function words_string changed)
    -> publication date is retrieved and parsed
    -> name of the newspaper is retrieved

 .3 articles_containing_words.py
    The query needed adjusting because now the date is recorded in the article object, not issue.

 .4 article_xml_with_words.py
    The same as above --- the date is recorded by article, not issue. This query relies on article.words_string to be implemented accurately.
 
