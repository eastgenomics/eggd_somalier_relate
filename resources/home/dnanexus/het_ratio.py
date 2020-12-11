## Plots

#import matplotlib.pyplot as plt
import numpy as np
#from mpldatacursor import datacursor
import pandas as pd
#from matplotlib.colors import ListedColormap


#### Read data in
data = pd.read_csv('somalier.samples.tsv', sep='\t')
dat = data.iloc[:,np.r_[1,18:25]] #select columns of interest

#### Create the Xhet_homo_ratio table and append to data frame
het_ratio = dat.iloc[:,4]/dat.iloc[:,5] 
het_ratio = pd.DataFrame({'X_het/X_homo_alt_ratio':het_ratio}) 
data2 = pd.concat([data, het_ratio], axis=1)

#### Add Predicted Sex based on Xhet_homo_ratio
PredictedSex = []
het_ratio = data2['X_het/X_homo_alt_ratio']
cutoff  = 0.6 #based on Peddy but can be changed 

for x in het_ratio:
    if x < cutoff:
        PredictedSex.append("M")
    else:
        PredictedSex.append("F")

Predicted_Sex = pd.DataFrame({'Predicted_Sex':PredictedSex}) 


##### Append Predicted Sex to dataframe and save replace the file
data3 = pd.concat([data2, Predicted_Sex], axis=1)
print(data3)
data3.to_csv('somalier.samples.tsv', sep='\t',index=False, header =True)

##### Plotting

# plt.scatter(x=data['X_het'],y=data['X_depth_mean'], color=cols)
# plt.ylabel("X depth mean")
# plt.xlabel("X heterozygote calls")
# datacursor(hover=True, point_labels=data['sample_id'])
# plt.show()


