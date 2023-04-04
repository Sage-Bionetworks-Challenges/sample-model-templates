library(optparse)
library(readr)
library(tidyr)

# Create a CLI ------------------------------------
# Two args: `input_dir`, `output_dir`
option_list <- list(
  make_option("--input_dir", type="character", default="/input", metavar="character"),
  make_option("--output_dir", type="character", default="/output", metavar="character")
)
opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)


# Read in input file ------------------------------
data <- read_csv(file.path(opt$input_dir, "names.csv"), col_types = "c")


# Run a prediction --------------------------------
# Full name only contains two names.
predictions <- extract(data, name, into=c("name", "first", "last"), "((.*?) (.*))")


# Output predictions to output file ---------------
write_csv(predictions, file.path(opt$output_dir, "predictions.csv"))
