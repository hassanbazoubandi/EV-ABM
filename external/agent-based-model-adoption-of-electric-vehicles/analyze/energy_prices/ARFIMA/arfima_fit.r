# install.packages("arfima")

library("arfima")
# set.seed(8564)
# sim <- arfima.sim(1000, model = list(phi = c(0.2, 0.1), dfrac = 0.4, theta = 0.9))
# fit <- arfima(sim, order = c(2, 0, 1), back=TRUE)

dane <- read.csv("data/eurpln_d.csv")
# print(dane$Zamkniecie)
fit <- arfima(dane$Zamkniecie, order = c(2, 0, 1), back=TRUE, quiet=TRUE)

save(fit, file = "energy_params.Rdata")
