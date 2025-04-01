# R Model Example

library(optparse)
library(readr)
library(dplyr)

predict <- function(df) {
  #' Sample prediction function.
  #'
  #' TODO: Replace this with your actual model prediction logic. In this
  #' example, random floats are assigned.
  #'
  #' @param df A data frame.
  #' @return A data frame with predictions.

  pred <- df %>% select(id)
  pred$probability <- runif(nrow(pred))
  pred
}

# Create a CLI ------------------------------------
# Two args: `input-dir`, `output-dir`
option_list <- list(
  make_option("--input-dir", type="character", default="/input", metavar="character"),
  make_option("--output-dir", type="character", default="/output", metavar="character")
)
opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)


# Read in input file ------------------------------
data <- read_csv(file.path(opt[["input-dir"]], "data.csv"), show_col_types = FALSE)


# Run a prediction --------------------------------
# Randomly generate a float between [0.0, 1.0)
predictions <- predict(data)


# Output predictions to output file ---------------
write_csv(predictions, file.path(opt[["output-dir"]], "predictions.csv"))
