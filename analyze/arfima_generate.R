library("arfima")

# set.seed(82365)
N <- 1000
model <- list(theta = 0.9, phi = 0.5, dfrac = 0.4)
sim <- arfima.sim(N, model = model)

df = data.frame(sim0=sim)
for (i in 1:99) {
  df[sprintf("sim%d", i)] <- arfima.sim(N, model = model)
}

write.csv(df, "tmp.csv", row.names=FALSE)
