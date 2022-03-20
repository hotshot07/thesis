import pandas as pd 
import matplotlib.pyplot as plt


data = pd.read_csv('possible_good.csv')


plt.hist(data['score'], bins = 500)
plt.show()

print(data['score'].describe().apply(lambda x: format(x, 'f')))

nmap_df = data[data["ip.dst"] == '89.100.107.148']

# plt.hist(nmap_df['score'], bins = 500)
# plt.show()

print()

print(nmap_df['score'].describe().apply(lambda x: format(x, 'f')))