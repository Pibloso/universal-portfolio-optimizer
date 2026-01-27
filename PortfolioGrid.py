
from DataImportYH import np
from DataImportYH import plt
from DataImportYH import returns

step = 0.01
weights = []

for w_vxc in np.arange(0, 1/0.3 + step, step):
    for w_vmo in np.arange(0, 1/0.3 + step, step):
        w_cash = 1 - w_vxc - w_vmo
        if w_cash >1 or w_vxc + w_vmo > 1/0.3:
            continue
        weights.append((w_vxc, w_vmo, w_cash))

portfolio_log_returns = []
for w_vxc, w_vmo, w_cash in weights:
    port_log_return = (
        w_vxc * returns['VXC.TO'] +
        w_vmo * returns['VMO.TO']
        )
    if w_cash >=0:
        port_log_return += w_cash * returns['CASH']
    else: port_log_return -= w_cash * returns['BORROW']
    cum_log_wealth = port_log_return.cumsum()
    portfolio_log_returns.append(cum_log_wealth)

print(len(portfolio_log_returns),len(weights))

final_wealths = np.array([])
for i, p in enumerate(portfolio_log_returns):
    if weights[i][2]<0 and np.min(p) <= .3 - 1 / (-weights[i][2] + 1):
        final_wealths = np.append(final_wealths, 0)
    else: final_wealths = np.append(final_wealths, p.iloc[-1])
wavg = final_wealths / np.sum(final_wealths)
best_weights = np.average(weights, axis=0, weights=wavg)
print(f"Best Allocation VXC:{best_weights[0]}, VMO: {best_weights[1]}, CASH: {best_weights[2]}")
