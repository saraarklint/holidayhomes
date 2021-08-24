# holidayhomes
I've been following the holiday home market in Rørvig for 10 years now, and I've decided to dig into data from the Danish real-estate website boliga.dk to:

* See if it's true what my mom says about many of the holiday homes staying in the same families, and if so, see if they have something in common.
* Use machine learning (smaller neural network in TensorFlow Keras) to predict price change and listing time. This seems a bit tricky with the amount of data I have, but I have some ideas that I look forward to trying out.
* Figure out how rare my dream holiday home is. Where are the holiday homes located that satisfy all my criteria, how often are they for sale, and are they more or less expensive than other holiday homes? This will come in handy next time I notice one for sale.
* See if I'm right that one of the real-estate agents in the area is acting differently than the others, and that out-of-town real-estate agents grossly underestimate the market prices.

This is quite some project, or perhaps rather projects, so I won't do everything at once. Investigating and fixing data issues, and deciding how to restructure data, has been a bit time-consuming so far.

<!--
As a way of practising obtaining, handling, and analyzing data in Python, I'm investigating the holiday home market in R&oslash;rvig, Denmark by looking at data from the Danish real-estate website boliga.dk.
Basically, I'm:

* Getting data from web APIs, and then investigating and fixing issues, and restructuring data.
* Describing the typical holiday home and the typical holiday home sale. Also, how rare is my ideal holiday home, and how often is it for sale?
* Using machine learning (smaller neural network in TensorFlow Keras) to predict price change and listing time.
-->

I've put some recurring things (mainly relating to boliga.dk's web APIs) into `boliga.py`, but the rest is divided into iPython Notebooks:

* `gettingdata.ipynb`: What web APIs at boliga.dk that's relevant for us to call, how to call them, and what their response is. Also a few preliminary looks at the data. (I've decided to get all data from boliga.dk, since sites like ois.dk don't allow automated requests while boliga.dk does.)