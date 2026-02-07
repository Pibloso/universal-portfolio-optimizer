
from DataImportYH import np, pd, tickers
from rich.progress import Progress

margin_limit = int(100//.3)
tickers.append('CASH')
returns = pd.read_pickle('YHData.pkl')
progress = Progress()

def cumulative_return(count):
    if weights['CASH'].iloc[count] >= 0:
        reference = 'CASH'
    else: reference = 'BORROW'
    returns['log_return'] = (
        np.cumsum(weights['VUN.TO'].iloc[count] * returns['VUN.TO']) +
        np.cumsum(weights['VMO.TO'].iloc[count] * returns['VMO.TO']) +
        np.cumsum(weights['VYMI'].iloc[count] * returns['VYMI']) +
        np.cumsum(weights['CASH'].iloc[count] * returns[reference])
    )
    progress.update(p_id, advance=1)
    if np.min(returns['log_return']) > -1:
        return np.max(returns['log_return'].iloc[-1], 0)
    else: return 0

def weight_matrix():
    weight_list = []
    for w_1 in range(margin_limit):
        for w_2 in range(margin_limit - w_1):
            for w_3 in range(margin_limit - w_1 - w_2):
                w_cash = 100 - w_1 - w_2 - w_3
                if w_cash >=100 or w_1 + w_2 + w_3 > margin_limit:
                    continue
                weight_list.append((w_1, w_2, w_3, w_cash))
    df = pd.DataFrame(weight_list, columns = tickers)
    return df, len(weight_list)


if __name__ == '__main__':
    weights, run_time = weight_matrix()
    print(weights)
    progress.start()
    p_id = progress.add_task("Calculating Returns:", total = run_time)
    weights['wealth'] = list(map(cumulative_return, range(run_time)))
    progress.stop()
    del returns

    weights['wavg'] = weights['wealth'] / np.sum(weights['wealth'])
    best_weights = np.average(weights, axis=0, weights=weights['wavg'])
    print(f"Best Allocation {tickers[0]}: {best_weights[0]}, {tickers[1]}: {best_weights[1]}, {tickers[2]}: {best_weights[2]}, CASH: {best_weights[3]}")
