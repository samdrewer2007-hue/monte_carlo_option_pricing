import numpy as np
import matplotlib.pyplot as plt
random_seed = 32
rng = np.random.default_rng(random_seed)
p_init = 100
time_to_maturity = 1
strike_price = 110
risk_free_rate = 0.05
volatility = 0.2
num_simulations = 10



def monte_carlo_option_pricing(p_init, strike_price, time_to_maturity, risk_free_rate, volatility, num_simulations, random_seed):
    num_steps = int(time_to_maturity * 252)  # Assuming 252 trading days in a year
    daily_shocks = rng.standard_normal(size = (num_simulations, num_steps)) * volatility * np.sqrt(1 / ((num_steps)/time_to_maturity))
    print(daily_shocks [0, :], 'daily_shocks')
    print(np.mean(daily_shocks), 'mean daily_shocks')
    prices = np.zeros((num_simulations, num_steps + 1))
    prices[:, 0] = p_init
    for column in range(num_steps):
        prices[:, column + 1] = prices[:, column] * np.exp(((risk_free_rate) - 0.5 * volatility ** 2) * (time_to_maturity / num_steps) + daily_shocks[:, column])
    return prices



stock_data =monte_carlo_option_pricing(p_init, strike_price, time_to_maturity, risk_free_rate, volatility, num_simulations, random_seed)
print(stock_data)
final_prices = stock_data[:, -1]
for i in range(num_simulations):
    plt.plot(np.arange(time_to_maturity * 252 + 1), stock_data[i], alpha=0.5)
plt.show()
