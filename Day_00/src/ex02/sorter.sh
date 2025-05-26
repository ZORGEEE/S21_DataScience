#!/bin/bash  

FILE="../ex01/hh.csv"  
{  
  # Выводим заголовки  
  head -n 1 $FILE  
  # Сортируем данные, пропуская заголовок  
  tail -n +2 $FILE | sort -t, -k2,2 -k1,1n  
} > hh_sorted.csv