#!/bin/bash

convert -density 300 -background white -alpha remove data_collection.pdf -quality 90 ../../docs/data_collection.png
convert -density 300 -background white -alpha remove modeling.pdf -quality 90 ../../docs/modeling.png
convert -density 300 -background white -alpha remove productionalization_feature_engineering.pdf -quality 90 ../../docs/productionalization_feature_engineering.png
convert -density 300 -background white -alpha remove productionalization_scoring.pdf -quality 90 ../../docs/productionalization_scoring.png
convert -density 300 -background white -alpha remove data_flow.pdf -quality 90 ../../docs/img/data_flow.png
