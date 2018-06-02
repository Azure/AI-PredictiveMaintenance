#!/bin/bash

convert -density 300 -background white -alpha remove data_collection.pdf -quality 90 data_collection.png
convert -density 300 -background white -alpha remove modeling.pdf -quality 90 modeling.png
convert -density 300 -background white -alpha remove productionalization_feature_engineering.pdf -quality 90 productionalization_feature_engineering.png
convert -density 300 -background white -alpha remove productionalization_scoring.pdf -quality 90 productionalization_scoring.png

