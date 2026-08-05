import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

random_seed = 42
p_init = 100
time_to_maturity = 1
strike_price = 110
risk_free_rate = 0.05
volatility = 0.2
num_simulations = 100000
theoretical_mean = p_init * np.exp(risk_free_rate * time_to_maturity)



def simulate_stock_paths(p_init, time_to_maturity, risk_free_rate, volatility, num_simulations, random_seed):
    num_steps = int(time_to_maturity * 252)  # Assuming 252 trading days in a year
    dt = time_to_maturity / num_steps
    rng = np.random.default_rng(random_seed)
    daily_shocks = rng.standard_normal(size = (num_simulations, num_steps)) * volatility * np.sqrt(dt)
    prices = np.zeros((num_simulations, num_steps + 1))
    prices[:, 0] = p_init
    for column in range(num_steps):
        prices[:, column + 1] = prices[:, column] * np.exp(((risk_free_rate) - 0.5 * volatility ** 2) * dt + daily_shocks[:, column])
    return prices


def black_scholes_call_price(p_init, strike_price, time_to_maturity, risk_free_rate, volatility):
    d1 = (np.log(p_init / strike_price) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    call_price = p_init * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
    return call_price

fig, axs = plt.subplots(4, 1, figsize=(10, 12))

stock_data =simulate_stock_paths(p_init, time_to_maturity, risk_free_rate, volatility, num_simulations, random_seed)
bs_call_price = black_scholes_call_price(p_init, strike_price, time_to_maturity, risk_free_rate, volatility)
final_prices = stock_data[:, -1]
mean_price = np.mean(final_prices)
payoffs = np.maximum(final_prices - strike_price, 0)  
zero_payoff_count = np.sum(payoffs == 0)
discounted_payoffs = np.exp(-risk_free_rate * time_to_maturity) * payoffs
mean_discounted_payoff = np.mean(discounted_payoffs)
stdev_discounted_payoff = np.std(discounted_payoffs, ddof=1)
stderr_discounted_payoff = stdev_discounted_payoff / np.sqrt(num_simulations)

running_mean = np.cumsum(discounted_payoffs) / np.arange(1, num_simulations + 1)

print(f'Theoretical mean final stock price: {theoretical_mean}')
print(f"Mean discounted payoff (Monte Carlo): {mean_discounted_payoff} ± {stderr_discounted_payoff}")
print(f"Black-Scholes call price: {bs_call_price}")
print(f"95% confidence interval for discounted payoff: ({mean_discounted_payoff - 1.96 * stderr_discounted_payoff}, {mean_discounted_payoff + 1.96 * stderr_discounted_payoff})")
confidence_interval = (mean_discounted_payoff - 1.96 * stderr_discounted_payoff, mean_discounted_payoff + 1.96 * stderr_discounted_payoff)
# set up necessary variables for option pricing


for i in range(min(50, num_simulations)):    #plot paths
    axs[0].plot(np.arange(time_to_maturity * 252 + 1), stock_data[i*len(stock_data)//50], alpha=0.5)  #select 50 evenly spaced paths from the total simulations
axs[0].set_title('Stock Price Paths (sample of 50 out of ' + str(num_simulations) + ' simulations)')
axs[0].set_xlabel('Trading Day')
axs[0].set_ylabel('Price')
axs[0].set_xlim([0, time_to_maturity * 252])

axs[1].hist(final_prices, bins=75, alpha=0.7, color='blue', edgecolor='black')   #final price histogram
axs[1].axvline(x = p_init, color='black', linestyle='--', label='Initial Price')
axs[1].axvline(x=theoretical_mean, color='orange', label='Theoretical Mean Price')
axs[1].axvline(x=mean_price, color='green', linestyle='--', label='Mean Final Price')
axs[1].axvline(x=strike_price, color='red', linestyle='--', label='Strike Price')
axs[1].set_title('Distribution of Final Stock Prices')
axs[1].set_xlabel('Final Price')
axs[1].set_ylabel('Frequency')
axs[1].set_xlim([0, np.percentile(final_prices, 99.5)])  # Limit x-axis to the 99.5th percentile to avoid extreme outliers
axs[1].legend()

positive_payoffs = payoffs[payoffs > 0]
if len(positive_payoffs) == 0:
    print("No positive payoffs were generated in the simulations.")
else:
    axs[2].hist(positive_payoffs, bins = 75, alpha=0.7, color='orange', edgecolor='black')   #payoff histogram
    axs[2].set_xlim([0, np.percentile(positive_payoffs, 99.5)]) # Limit x-axis to the 99.5th percentile to avoid extreme outliers
    axs[2].set_title(f'Distribution of Positive Payoffs ({(zero_payoff_count/num_simulations) * 100:.2f}% of simulations resulted in zero payoff).')
    axs[2].set_xlabel('Payoff')
    axs[2].set_ylabel('Frequency')


axs[3].plot(running_mean, color='blue')
axs[3].set_title('Convergence of Monte Carlo Estimate to Black-Scholes Call Price')
axs[3].set_xlabel('Simulation')
axs[3].set_ylabel('Running Mean')

margin = 2
axs[3].set_xlim(100, num_simulations)  # Set x-axis limit to the number of simulations
axs[3].set_ylim(bs_call_price - margin, bs_call_price + margin)  
axs[3].set_xscale('log')  # Set x-axis to logarithmic scale for better visualization of convergence
axs[3].axhline(y = bs_call_price, color = 'black', linestyle = '--', label = 'Black-Scholes Call Price')
axs[3].legend()
axs[3].grid(True, which="both", alpha=0.3)

plt.tight_layout()
plt.savefig('monte_carlo_option_pricing.png', dpi = 300, bbox_inches = 'tight')
plt.show()
