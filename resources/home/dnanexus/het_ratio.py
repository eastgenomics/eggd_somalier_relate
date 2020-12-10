## Plots

#import matplotlib.pyplot as plt
import numpy as np
#from mpldatacursor import datacursor
import pandas as pd
#from matplotlib.colors import ListedColormap


data = pd.read_csv('somalier.samples.tsv', sep='\t')
dat = data.iloc[:,np.r_[1,18:25]]
print(dat)

het_ratio = dat.iloc[:,4]/dat.iloc[:,5]
print(het_ratio)
#dat.join(het_ratio)

het_ratio = pd.DataFrame({'X_het/X_homo_alt_ratio':het_ratio}) 
data2 = pd.concat([data, het_ratio], axis=1)

data2.to_csv('somalier.samples.tsv', sep='\t',index=False, header =True)

# colnames = dat2.columns
# print(colnames)

# dat2 = dat.iloc[:,np.r_[1,4]]
# print(dat2)

#color based on given information - create a random string of red and blue
# stated_sex = ["male", "male", "female", "female"] + ["male"]*7
# cols = []
# for i in stated_sex:
#     if i == "male":
#         cols.append( "blue")
#     else:
#         cols.append("red")


# plt.scatter(x=data['X_het'],y=data['X_depth_mean'], color=cols)
# plt.ylabel("X depth mean")
# plt.xlabel("X heterozygote calls")
# datacursor(hover=True, point_labels=data['sample_id'])
# plt.show()


