#!bin/bash
wget -m --convert-links --page-requisites https://v-sense.scss.tcd.ie/Datasets/DublinCity/DublinCityAll.tar.gz 

mkdir bin_data && tar xf DublinCityAll.tar.gz -C bin_data --strip-components 1
