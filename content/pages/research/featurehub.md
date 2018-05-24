Title: FeatureHub
status: hidden
url: research/FeatureHub
save_as: research/FeatureHub.html

[*FeatureHub*](https://hdi-project.github.io/FeatureHub) is a new paradigm for collaborative
feature engineering and an associate proof-of-concept cloud platform. In our approach,
independent data scientists collaborate on a feature engineering task, viewing and
discussing each others’ features in real-time.  Feature engineering source code created by
independent data scientists is then integrated into a single predictive machine learning
model. Our platform includes an automated machine learning backend which abstracts model
training, selection, and tuning, allowing users to focus on feature engineering while still
receiving immediate feedback on the performance of their features.

Here are slides from my presentation at IEEE DSAA 2017.

<!--
 Adapted from pdf.js demo.
 Source: https://mozilla.github.io/pdf.js/examples/
  -->
<div>
  <button id="prev">Previous</button>
  <button id="next">Next</button>
  &nbsp; &nbsp;
  <span>Page: <span id="page_num"></span> / <span id="page_count"></span></span>
</div>

<canvas id="the-canvas" style="border: 1px solid black;"></canvas>

<!-- Retarded trick to get pelican to link to file -->
<div style="display: none;">
<a id='url-junk' href='{filename}/files/featurehub-dsaa-presentation-oct-2017.pdf'></a>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.0.489/pdf.min.js"></script>
<script>
    // If absolute URL from the remote server is provided, configure the CORS
    // header on that server.
    var element=document.getElementById("url-junk");
    var url=element.href;
</script>
<script src="{filename}/extra/slides.js"></script>
