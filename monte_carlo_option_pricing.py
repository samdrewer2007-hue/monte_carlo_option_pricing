import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

random_seed = 23
rng = np.random.default_rng(random_seed)
p_init = 100
time_to_maturity = 1
strike_price = 110
risk_free_rate = 0.05
volatility = 0.2
num_simulations = 10000
sim_mean = p_init * np.exp(risk_free_rate * time_to_maturity)



def monte_carlo_option_pricing(p_init, strike_price, time_to_maturity, risk_free_rate, volatility, num_simulations, random_seed):
    num_steps = int(time_to_maturity * 252)  # Assuming 252 trading days in a year
    dt = time_to_maturity / num_steps
    rng = np.random.default_rng(random_seed)
    daily_shocks = rng.standard_normal(size = (num_simulations, num_steps)) * volatility * np.sqrt(dt)
    prices = np.zeros((num_simulations, num_steps + 1))
    prices[:, 0] = p_init
    for column in range(num_steps):
        prices[:, column + 1] = prices[:, column] * np.exp(((risk_free_rate) - 0.5 * volatility ** 2) * (time_to_maturity / num_steps) + daily_shocks[:, column])
    return prices


def black_scholes_call_price(p_init, strike_price, time_to_maturity, risk_free_rate, volatility):
    d1 = (np.log(p_init / strike_price) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    call_price = p_init * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
    return call_price

fig, axs = plt.subplots(3, 1, figsize=(10, 6))

stock_data =monte_carlo_option_pricing(p_init, strike_price, time_to_maturity, risk_free_rate, volatility, num_simulations, random_seed)
bs_call_price = black_scholes_call_price(p_init, strike_price, time_to_maturity, risk_free_rate, volatility)
final_prices = stock_data[:, -1]
mean_price = np.mean(final_prices)
payoffs = np.maximum(final_prices - strike_price, 0)  
mean_payoff = np.mean(payoffs) 
zero_payoff_count = np.sum(payoffs == 0)
discounted_payoffs = np.exp(-risk_free_rate * time_to_maturity) * payoffs
mean_discounted_payoff = np.mean(discounted_payoffs)
stdev_discounted_payoff = np.std(discounted_payoffs)
stderr_discounted_payoff = stdev_discounted_payoff / np.sqrt(num_simulations)
print(sim_mean)
print(f"Mean discounted payoff: {mean_discounted_payoff} ± {stderr_discounted_payoff}")
print(f"Black-Scholes call price: {bs_call_price}")
# set up necessary variables for option pricing


#for i in range(num_simulations):    #plot paths
#    axs[0].plot(np.arange(time_to_maturity * 252 + 1), stock_data[i], alpha=0.5)
axs[0].set_title('Stock Price Paths')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Price')
axs[0].set_xlim([0, time_to_maturity * 252])

#axs[1].hist(final_prices, bins=400, alpha=0.7, color='blue', edgecolor='black')   #final price histogram
axs[1].axvline(x = p_init, color='black', linestyle='--', label='Initial Price')
axs[1].axvline(x=sim_mean, color='orange', linestyle='--', label='Theoretical Mean Price')
axs[1].axvline(x=mean_price, color='green', linestyle='--', label='Mean Final Price')
axs[1].axvline(x=strike_price, color='red', linestyle='--', label='Strike Price')
axs[1].set_title('Distribution of Final Stock Prices')
axs[1].set_xlabel('Final Price')
axs[1].set_ylabel('Frequency')
axs[1].set_xlim([0, np.max(final_prices)])
axs[1].legend()

#axs[2].hist(payoffs, bins = 140, alpha=0.7, color='orange', edgecolor='black')   #payoff histogram
axs[2].set_xlim([0.01, sim_mean])

plt.tight_layout()
plt.savefig('monte_carlo_option_pricing.png')
plt.show()
