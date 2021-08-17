import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
# Get the data for the stock AAPL
ticker = 'AAPL'
dfa = yf.download(ticker,'2000-01-01','2021-07-01')
dfs = yf.download('^GSPC','2000-01-01','2021-07-01')
ax = dfa['Close'].plot(figsize=(20,12),label= ticker)
dfs['Close'].plot(ax=ax, secondary_y=True, label = 'SP500')
ax.legend(loc=2)
ax.set_title('Корреляция  актива по сравнению с  эталоном SP500')
plt.savefig('cor_SP500_'+ticker+'.png',dpi=150)
