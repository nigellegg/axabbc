# axabbc
Consume the RSS feed list from BBC and run NER.  For AXA Data Engineer role.  

1. Extraction of text uses Beautiful Soup - to strip out the javascript and the html tags.  
2. Then use spacy for named entity recognition; pulls out ent.text and ent.label_. 
3. For location entities, use Nominatim api - open street map, free geolocation api.  

Somewhere along the line, there is an error in the looping or saving.  This means that multiple copies of the text 
are bing analysed.  Will look at this tomorrow morning.  

