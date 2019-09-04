import numpy as np
from scipy import stats

x = np.linspace(1, 10, 10)

a = np.ones(10) * 2
b = np.ones(10) * 3
c = np.ones(10) * 4

b[7:] = np.nan
c[5:] = np.nan

abc = np.stack((a, b, c))

print("Arrays:")
print(abc)

print("Before masking:")
print(np.mean(abc, axis=0))

print("Before masking (nanmean):")
print(np.nanmean(abc, axis=0))

print("After masking:")
# abc_masked = np.ma.masked_where(np.isnan(abc), abc)
abc_masked = np.ma.MaskedArray(abc,
                               np.isnan(abc),
                               dtype=np.float,
                               fill_value=np.nan)

print(np.mean(abc_masked, axis=0))

xxx = np.stack((x, x, x))


print("Statistic: Before masking:")
statistic, bin_edges, _ = stats.binned_statistic(
    xxx.ravel(), abc.ravel(), statistic='mean', bins=x)
print(statistic)
# print(bin_edges)


print("Statistic: After masking:")
statistic, bin_edges, _ = stats.binned_statistic(
    xxx.ravel(), abc_masked.ravel(), statistic='mean', bins=x)
print(statistic)
# print(bin_edges)

print("Statistic: Before masking (nanmean):")
statistic, bin_edges, _ = stats.binned_statistic(
    xxx.ravel(), abc.ravel(), statistic=np.nanmean, bins=x)
print(statistic)
# print(bin_edges)


# print("Histogram: Before masking:")
# statistic, bin_edges = np.histogram(abc.ravel(), bins=x, weights=xxx.ravel())
# print(statistic)


# print("Histogram: After masking:")
# statistic, bin_edges = np.histogram(
#     abc_masked.ravel(), bins=x, weights=xxx.ravel())
# print(statistic)
