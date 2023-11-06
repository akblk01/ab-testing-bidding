import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

control = pd.read_excel("measurement_problems/datasets/ab_testing.xlsx", sheet_name="Control Group")
test = pd.read_excel("measurement_problems/datasets/ab_testing.xlsx", sheet_name="Test Group")

# degiskenler
# Impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

control.describe().T
test.describe().T

df = pd.concat([control, test], join="inner", ignore_index=True)

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi) Süreci
######################################################
# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direk 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.

############################
# 1. Hipotezi Kur
############################

# H0: M1 = M2 (kontrol veri setindeki purchase ile test veri setindeki purchase arasında is.anl. fark yok)
# H1: M1 != M2(... fark var)

control["Purchase"].mean()
test["Purchase"].mean()

############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı
# Varyans Homojenliği

############################
# Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# p-value = 0.1541 old. H0 REDREDDEDILEMEZ. Normal dağılım varsayımı sağlanmaktadır.

test_stat, pvalue = shapiro(control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# p-value = 0.5891 old. H0 REDREDDEDILEMEZ. Normal dağılım varsayımı sağlanmaktadır.

############################
# Varyans Homojenligi Varsayımı
############################

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(test["Purchase"],
                           control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# p-value = 0.1083 old. için  H0 REDDEDILEMEZ. Varyanslar homojendir

test_stat, pvalue = ttest_ind(test["Purchase"],
                              control["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# H0: M1 = M2 (kontrol veri setindeki purchase ile test veri setindeki purchase arasında is.anl. fark yok)
# H1: M1 != M2(... fark var)
# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
# p-value = 0.3493 old. için  H0 REDDEDILEMEZ.
# Yani; H1: M1 != M2(... fark var)