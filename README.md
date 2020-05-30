# covid-coverage
Collecting data about where Youtube related-videos lead you

I want to study how people interact with covid-related content on Youtube. From my own experience, one of the major ways I 
interact with Youtube as a platform is by watching one video and then watching subsequent videos that are listed as "related" 
to that one. The theory is this type of behavior could lead people down a rabbit hole of disinformation and radicalization. 
Youtube has a data api (found here: https://developers.google.com/youtube/v3/getting-started (Links to an external site.)). In 
that api, it has a search command, for which you can use the 'relatedToVideoId' parameter. More information about that command 
is found here: https://developers.google.com/youtube/v3/docs/search/list?apix_params=%7B%22part%22%3A%22snippet%22%2C%22maxResults%22%3A25%2C%22q%22%3A%22covid-19%22%2C%22safeSearch%22%3A%22none%22%7D (Links to an external site.).

 

The proposed procedure is this:

Enter a top-level search using a covid-related keyword. This could be 'covid-19' or 'coronavirus' or 'corona pandemic' or 
something similar. Use the top 5 results from this search as the seed nodes in our network. From these nodes, conduct a 
breadth first search, adding the first 5 related videos of those seed nodes as neighbors and bubbling out from there. For each 
step, capture as much information about the video as we can. This could include the number of views, the category, the title, 
etc. I'll extend as many levels deep as I can, rate-limiter permitting. 

 

With this network created, there are a few different types of analysis that can be performed. We can see how many cycles show 
up. We can compare the content of the seeds to the content each level out and see how they change. We can try to determine if 
there are distinct 'bubbles' that exist within coverage along partisan lines. I'll try to shift my analysis to match the type 
and amount of data I can gather.
