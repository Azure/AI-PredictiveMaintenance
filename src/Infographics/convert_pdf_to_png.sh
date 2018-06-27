#!/bin/bash

convert -density 150 -background white -alpha remove data_flow.pdf -quality 90 data_flow.png
convert -density 90 -background white -alpha remove data_collection.pdf -quality 90 data_collection.png
convert -density 150 -background white -alpha remove modeling.pdf -quality 90 modeling.png
convert -density 90 -background white -alpha remove productionalization_feature_engineering.pdf -quality 90 productionalization_feature_engineering.png
convert -density 90 -background white -alpha remove productionalization_scoring.pdf -quality 90 productionalization_scoring.png


cp data_collection.png modeling.png productionalization_feature_engineering.png productionalization_scoring.png data_flow.png ../../docs/img/