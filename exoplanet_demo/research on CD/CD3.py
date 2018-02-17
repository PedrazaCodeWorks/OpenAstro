#%matplotlib qt/inline
import pylab as plt
import seaborn as sns
import pandas as pd
import numpy as np
#sns.set(style="darkgrid")
df = pd.read_csv('circumstellardisks.csv')

#df.describe(include='all')
#df.columns
#numcol=len(df.columns)
#col=list(df.columns)
##See number counts per Category
categories = df.Category.value_counts()
##make a list of Category
diskCategory=list(categories.index)
#list(df.['Spec Type'].value_counts().index) shows too much categories

##See Spec Types
SpecTypeCategory = list(df['Spec Type'])
##narrow down category by letters i.e. A, B, ... only and save as new column in df
df.loc[df['Spec Type'].notnull(), 'Spec Type Index'] = df['Spec Type'].str[0] #str[:2]
##recount Spec Type Category
SpecTypeCategory = list(df['Spec Type Index'].value_counts().index)


'''
basic plots
'''
plt.figure(1)
sns.countplot(x="Category", data=df, order=diskCategory, palette="Greens_d")

plt.figure(2)
#sns.countplot(x=SpecTypeCategory, data=SpecCount, palette="Greens_d", order=SpecTypeCategory)
sns.countplot(x='Spec Type Index', data=df, order=['B','A','F','G','K','M'], palette="Greens_d")

'''
Count per wavelength interval
> 1000 μm, 100-1000 μm, 1-10 μm, 0.1-1 μm
'''
upTo1 = sum(item < 1 for item in df['At ref. wavelength (microns)'])
OneTo10 = sum(item > 1 and item < 10 for item in df['At ref. wavelength (microns)'])
TenTo100 = sum(item > 10 and item < 100 for item in df['At ref. wavelength (microns)'])
HundredTo1000 = sum(item > 100 and item < 1000 for item in df['At ref. wavelength (microns)'])
MoreThan1000 = sum(item > 1000 for item in df['At ref. wavelength (microns)'])

wavelengthCount = {'upTo1':upTo1,'OneTo10':OneTo10,'TenTo100':TenTo100, 
                   'HundredTo1000':HundredTo1000,'MoreThan1000':MoreThan1000}
wavelengthRange = ['<1','1-10', '10 - 100', '100 - 1000','>1000']

##ADD:show spectral type division in each bar
plt.figure(3)
X = np.arange(len(wavelengthRange))
plt.bar(X, wavelengthCount.values(), align='center', width=0.5)
plt.xticks(X, wavelengthRange)
ymax = max(wavelengthCount.values()) + 1
plt.ylabel('Count')
plt.xlabel('wavelength range')
plt.ylim(0, ymax)
plt.show()

#df.plot(kind='bar', stacked='True')

plt.figure(4)
plt.loglog(df['Disk Diameter (AU)'], df['Distance (pc)'], 'o')
plt.xlabel('Disk Diameter (AU)')
plt.ylabel('Distance (pc)')

plt.figure(5)
plt.loglog(df['At ref. wavelength (microns)'], df['Disk Diameter (AU)'], 'o')
plt.ylabel('Disk Diameter (AU)')
plt.xlabel('Wavelength (microns)')

##Plot with size as another parameter
#df.plot(kind='scatter', x='Disk Major Axis &quot;', y='At ref. wavelength (microns)', s=df['Disk Diameter (AU)']);
#df.plot(kind='hexbin', x='X', y='Y', gridsize=25)

plt.figure(6)
labels = ['B','A','F','G','K','M']
mapping = {'B': 0,'A': 1,'F': 2,'G': 3,'K': 4,'M': 5}
df = df.replace({'Spec Type Index': mapping})
fig = plt.subplots()
ax1 = plt.gca()
ax1.scatter(df['Spec Type Index'], df['Disk Diameter (AU)'])
plt.ylabel('Disk Diameter (AU)')
plt.xlabel('Spectral Type')
plt.xticks(range(len(labels)), labels)
ax1.set_yscale('log')

###stratify fig 6 by wavelength range
##create a new column that classify wavelength in group
df['wavelength range']=0
i=0
for item in df['At ref. wavelength (microns)']:
    if item < 1:
        df['wavelength range'][i]=1 #group 1   
    elif item > 1 and item < 10:
        df['wavelength range'][i]=2 #2
    elif item > 10 and item < 100:
        df['wavelength range'][i]=3 #3
    elif item > 100 and item < 1000:
        df['wavelength range'][i]=4 #4
    elif item > 1000:
        df['wavelength range'][i]=5 #5
    else: #nan
        df['wavelength range'][i]=0 #5
    i+=1

labels = ['B','A','F','G','K','M']
##encode spectral class into int so that it can be grouped
mapping = {'B': 0,'A': 1,'F': 2,'G': 3,'K': 4,'M': 5}
df = df.replace({'Spec Type Index': mapping})
##wranges for legend; to get size of circle, use
#df['Disk Diameter (AU)'][df['Spec Type Index']==4][df['wavelength range']==2]
wranges= ['<1 μm','1-10 μm','10-100 μm','100-1000 μm','>1000 μm']
colors = ['k','r','y','g','b']
##wavelength groups [0:5]
groups = sorted(list(set(df['wavelength range'].values)))

plt.figure(7)
ax2 = plt.gca()
##s=df['Disk Diameter (AU)']/10 refers to size of items
for group, color in zip(groups,colors):
    plt.scatter(df['Spec Type Index'][df['wavelength range']==group],
             df['Disk Diameter (AU)'][df['wavelength range']==group],
             marker='o', color=color)             
ax2.set_yscale('log')
plt.legend(wranges, frameon='True', loc=8)#'upper left')
ax2.get_legend().get_frame().set_facecolor('w') 
plt.ylabel('Disk Diameter (AU)')
plt.xlabel('Spectral Type')
plt.xticks(range(len(labels)), labels)
ax3 = ax2.twinx()
ax3.scatter(3,170, marker='^',color='r') #G=3@H-band,  disk major axis=170AU
ax3.text(3.2, 169, 'SU Aur')
#ax3.annotate('SU Aur', xy=(3.2, 168)) 
ax3.axes.get_yaxis().set_ticks([]) #hide axis so that no overlap with ax2
