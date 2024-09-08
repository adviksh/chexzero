library(here)
library(tibble)
library(readr)
library(fst)

all_names   = read_lines(here('data', 'IMAGE_FILENAMES.txt'))
study_first = read_fst(here('data', 'study_with_lab_heart_pending.fst'))

all_names = tibble(file     = read_lines(here('data', 'IMAGE_FILENAMES.txt')),
                   study_id = as.integer(substr(file, 22, 29)))
sub_names = dplyr::inner_join(all_names, study_first, by = "study_id")

write_lines(unique(sub_names$file), here('data', 'PENDING_LAB_NAMES.txt'))