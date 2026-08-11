# Monte Carlo Option Pricing
## Overview
This project simulates the price paths of a given number of stocks in a Monte Carlo simulation, accounting for risk-free growth and daily volatlilty. THe final price of these is then used to determine the payoff from a European call option for this stock. This MOnte Carlo price is then compared to the analytical Black-Scholes call price, with quantified standard errors and a 95% confidence interval.

## Stock price modelling
This project models the stock price through geometric Brownian motion. 

$$
S_{t+\Delta t}
=
S_t \exp\left[
\left(r-\frac{1}{2}\sigma^2\right)\Delta t
+
\sigma\sqrt{\Delta t}Z
\right]
$$