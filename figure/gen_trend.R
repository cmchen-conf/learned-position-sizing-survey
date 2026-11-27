# Publication trend of the 95 studies by year and taxonomy branch (Fig. trend of the CSUR draft v0.3).
# Data: year_branch.csv, written by ../scripts/make_tables.py from coding.csv (final_decision = include).
# Palette (v0.7.1): four hues with clearly separated lightness (relative luminance 0.03 / 0.14 / 0.30 / 0.65), so the branches stay distinct in greyscale print;
# totals are printed above each bar, so identity and size never rest on colour alone.
# Usage: Rscript gen_trend.R   (run inside figure/); output trend.pdf, native size 4.75 x 2.0 in, vector.
suppressPackageStartupMessages(library(ggplot2))
d <- read.csv("year_branch.csv")
lab <- c(A = "A predict-then-size", B = "B learn-to-size", C = "C size as an RL action", D = "D size set by a language model")
d$branch <- factor(d$branch, levels = c("D", "C", "B", "A"))
tot <- aggregate(n ~ year, d, sum)
p <- ggplot(d, aes(factor(year), n, fill = branch)) +
  geom_col(width = 0.72, colour = "white", linewidth = 0.3) +
  geom_text(data = tot, aes(factor(year), n, label = n), inherit.aes = FALSE, vjust = -0.35, size = 2.8) +
  scale_fill_manual(values = c(A = "#16325c", B = "#b5452f", C = "#4aa38f", D = "#f4cf6b"),
                    labels = lab, breaks = c("A", "B", "C", "D"), name = NULL) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.12)), breaks = seq(0, 25, 5)) +
  labs(x = "Publication year (2026 partial)", y = "Studies") +
  theme_minimal(base_size = 8.5) +
  theme(legend.position = c(0.02, 0.98), legend.justification = c(0, 1), legend.key.size = unit(7, "pt"),
        legend.text = element_text(size = 7.5), legend.background = element_rect(fill = "white", colour = NA),
        panel.grid.major.x = element_blank(), panel.grid.minor = element_blank(),
        axis.text = element_text(size = 7.5, colour = "black"))
ggsave("trend.pdf", p, width = 4.75, height = 2.0, units = "in", device = cairo_pdf)
