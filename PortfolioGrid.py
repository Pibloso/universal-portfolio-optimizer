
from DataImportYH import np, pd
from rich.progress import Progress

weights = []
margin_limit = 100//.3

for w_1 in np.arange(0, margin_limit):
    for w_2 in np.arange(0, margin_limit - w_1):
        for w_3 in np.arange(0, margin_limit - w_1 - w_2):
            w_cash = 100 - w_1 - w_2 - w_3
            if w_cash >=100 or w_1 + w_2 + w_3 > margin_limit:
                continue
            weights.append((w_1, w_2, w_3, w_cash))

print(f"Grid complete: {len(weights)}")

portfolio_log_returns = []
returns = pd.read_pickle("YHData.pkl")

with Progress() as progress:
    bar1 = progress.add_task("Calculating Returns:", total=len(weights))

    for w in weights:
        port_log_return = (
            w_1 * returns['VUN.TO'] +
            w_2 * returns['VMO.TO'] +
            w_3 * returns['VYMI']
        )
        if w_cash >=0:
            port_log_return += w_cash * returns['CASH']
        else: port_log_return -= w_cash * returns['BORROW']
        del w
        portfolio_log_returns.append(port_log_return.cumsum())
        progress.update(bar1, advance=1)

del returns
print(len(portfolio_log_returns),len(weights))

final_wealths = np.array([])
for i, p in enumerate(portfolio_log_returns):
    if weights[i][3]<0 and np.min(p) <= .3 - 1 / (-weights[i][3] + 1):
        final_wealths = np.append(final_wealths, 0)
    else: final_wealths = np.append(final_wealths, p.iloc[-1])
wavg = final_wealths / np.sum(final_wealths)
best_weights = np.average(weights, axis=0, weights=wavg)
print(f"Best Allocation VUN:{best_weights[0]}, VMO: {best_weights[1]}, VYMI: {best_weights[2]}, CASH: {best_weights[3]}")
