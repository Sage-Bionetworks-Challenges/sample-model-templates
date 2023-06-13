if (!suppressWarnings(require("pacman", character.only = TRUE))) {
  install.packages("pacman", repos = "http://cran.us.r-project.org")
}

pkg_list <- c("optparse", "readr", "tidyr")

pacman::p_load(pkg_list, character.only = TRUE)
