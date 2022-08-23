
library(dplyr)
library(tidyr)
# compute unique ID's using cumsum
result <- read.csv('data_breaks.csv') %>% 
  mutate(Period = as.Date(Period, '%m/%d/%Y')) %>% 
  mutate(Return = 0.01 * as.numeric(gsub('%', '', Return))) %>% 
  mutate(BreakGroup = ifelse(is.na(Return) & !is.na(lag(Return)), 1, 0)) %>% 
  mutate(BreakGroup = cumsum(BreakGroup) + 1) %>% 
  drop_na(Return)

