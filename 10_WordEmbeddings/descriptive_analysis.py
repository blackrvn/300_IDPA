from utils import get_numbers
from icecream import ic
import matplotlib.pyplot as plt

num_affairs_by_party, num_tokens_by_party, num_affairs_by_legislativePeriod = get_numbers()

ic(num_affairs_by_legislativePeriod)
ic(num_affairs_by_party)
ic(num_tokens_by_party)

fig0, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
fig1, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
handles_0 = []
for legislativePeriod in num_affairs_by_legislativePeriod:
    handles_0.append(ax0.bar(legislativePeriod, num_affairs_by_legislativePeriod[legislativePeriod]))
for p in num_affairs_by_party:
    ax1.bar(p, num_affairs_by_party[p])

plt.show()
