

```python
from datetime import datetime as dt
print('Last accessed on: {}'.format(dt.now()))
```

    Last accessed on: 2016-11-29 16:12:36.411000



```python
from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''')
```




<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>



# Tutorial 1 
# Astronomy Series: Exoplanet Goldrush

In this tutorial, we will learn how to:
* access NASA website's data of all known exoplanets,
* create basic plots that describe their properties, and
* fit regression line to describe relationship between parameters.

Note: If you want to run the following Python scripts, please make sure you have Python and Jupyter notebook installed. If you are unsure how to do this, check out our [another tutorial](https://jpdeleon.github.io/2016-11-29-Python-Set-up/) on how to set-up your machine.

## About the database
The [NASA Exoplanet Archive](http://exoplanetarchive.ipac.caltech.edu/) provides data and various tools related to exoplanets. See for example the [table of confirmed exoplanet data here](http://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=planets).

While we can make scatter plots and histograms in the website, we would like to play with the data and do additional visualization and analysis. Thanks to their [API](https://en.wikipedia.org/wiki/Application_programming_interface), we can [query data from their website](http://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html) and print results directly to this notebook. 

Let's begin.

# Accessing data


```python
#for Pyton 2.7
import urllib2
import time

url = 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets'
response = urllib2.urlopen(url)
html = response.read()

outpath = 'confirmed_planets_{}.csv'.format(time.strftime("%Y%m%d")) #include date of download

print("retrieving URL: {}".format(url))

with open(outpath,'wb') as f:
     f.write(html)
print("created file: {}".format(outpath))
```

    retrieving URL: http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets
    created file: confirmed_planets_20161129.csv


What the code does above is use the `urllib2` library to request from NASA shown by the `url` variable. The response of NASA's API is saved into the variable called `response`. In this case it consists of data which we requested from the url. This data is only readable by machine so we have to read it using `response.read()` and save the read results into the `html` variable. We want to save the read data into our machine and name it `confirmed_planets_(date accessed)`. As seen above, the url and the filename is printed above.

Great! We downloaded the NASA's entire exoplanet database into a .csv file found in our local folder (filesize is 1.2 Mb). Above we used Python 2.7 but you can use Python 3.5 (newer version) to do the same task as shown below.


```python
#for python 3
import urllib.request 

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    html = response.read()

outpath = 'confirmed_planets_{}.csv'.format(time.strftime("%Y%m%d")) #include date of download

print("retrieving URL: {}".format(url))

with open(outpath,'wb') as f:
     f.write(html)
print("created file: {}".format(outpath))
```

Let's check the downloaded file. Since we expect that the data is huge, we only want print the first 500 characters.


```python
html[:500]
```




    'pl_hostname,pl_letter,pl_discmethod,pl_pnum,pl_orbper,pl_orbpererr1,pl_orbpererr2,pl_orbperlim,pl_orbpern,pl_orbsmax,pl_orbsmaxerr1,pl_orbsmaxerr2,pl_orbsmaxlim,pl_orbsmaxn,pl_orbeccen,pl_orbeccenerr1,pl_orbeccenerr2,pl_orbeccenlim,pl_orbeccenn,pl_orbincl,pl_orbinclerr1,pl_orbinclerr2,pl_orbincllim,pl_orbincln,pl_bmassj,pl_bmassjerr1,pl_bmassjerr2,pl_bmassjlim,pl_bmassn,pl_bmassprov,pl_radj,pl_radjerr1,pl_radjerr2,pl_radjlim,pl_radn,pl_dens,pl_denserr1,pl_denserr2,pl_denslim,pl_densn,pl_ttvflag,'



The data doesn't look pretty. Good thing Python has library that knows how to handle .csv (comma-separated values). In the following, we will use the Python library called [pandas](http://pandas.pydata.org/) to parse data among others.


```python
import pandas as pd
df = pd.read_csv(outpath)
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pl_hostname</th>
      <th>pl_letter</th>
      <th>pl_discmethod</th>
      <th>pl_pnum</th>
      <th>pl_orbper</th>
      <th>pl_orbpererr1</th>
      <th>pl_orbpererr2</th>
      <th>pl_orbperlim</th>
      <th>pl_orbpern</th>
      <th>pl_orbsmax</th>
      <th>...</th>
      <th>st_massblend</th>
      <th>st_massn</th>
      <th>st_rad</th>
      <th>st_raderr1</th>
      <th>st_raderr2</th>
      <th>st_radlim</th>
      <th>st_radblend</th>
      <th>st_radn</th>
      <th>pl_nnotes</th>
      <th>rowupdate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Kepler-139</td>
      <td>c</td>
      <td>Transit</td>
      <td>2</td>
      <td>157.072878</td>
      <td>0.001720</td>
      <td>-0.001720</td>
      <td>0.0</td>
      <td>3</td>
      <td>0.586</td>
      <td>...</td>
      <td>0.0</td>
      <td>2</td>
      <td>1.30</td>
      <td>0.25</td>
      <td>-0.25</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4</td>
      <td>1</td>
      <td>2014-05-14</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Kepler-140</td>
      <td>c</td>
      <td>Transit</td>
      <td>2</td>
      <td>91.353282</td>
      <td>0.001370</td>
      <td>-0.001370</td>
      <td>0.0</td>
      <td>3</td>
      <td>0.414</td>
      <td>...</td>
      <td>NaN</td>
      <td>1</td>
      <td>1.29</td>
      <td>0.24</td>
      <td>-0.24</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4</td>
      <td>1</td>
      <td>2014-05-14</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Kepler-141</td>
      <td>b</td>
      <td>Transit</td>
      <td>2</td>
      <td>3.107675</td>
      <td>0.000022</td>
      <td>-0.000022</td>
      <td>0.0</td>
      <td>2</td>
      <td>0.039</td>
      <td>...</td>
      <td>0.0</td>
      <td>2</td>
      <td>0.79</td>
      <td>0.04</td>
      <td>-0.04</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4</td>
      <td>1</td>
      <td>2014-05-14</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Kepler-141</td>
      <td>c</td>
      <td>Transit</td>
      <td>2</td>
      <td>7.010606</td>
      <td>0.000020</td>
      <td>-0.000020</td>
      <td>0.0</td>
      <td>3</td>
      <td>0.067</td>
      <td>...</td>
      <td>0.0</td>
      <td>2</td>
      <td>0.79</td>
      <td>0.04</td>
      <td>-0.04</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4</td>
      <td>1</td>
      <td>2014-05-14</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Kepler-142</td>
      <td>c</td>
      <td>Transit</td>
      <td>3</td>
      <td>4.761702</td>
      <td>0.000005</td>
      <td>-0.000005</td>
      <td>0.0</td>
      <td>3</td>
      <td>0.057</td>
      <td>...</td>
      <td>0.0</td>
      <td>2</td>
      <td>1.27</td>
      <td>0.24</td>
      <td>-0.24</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4</td>
      <td>1</td>
      <td>2014-05-14</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 80 columns</p>
</div>



After importing pandas with codename pd, we saved its result into variable `df` which stands for **dataframe**. We only print the head (i.e. first 5 items) of the dataframe showing 80 columns above. 

How about that? Look's pretty, right? Now we can make sense of this data. Basically we have the exoplanet's host name (meaning the parent star of the exoplanet) on the first column (e.g. HD 4308). The integers 0, 1, 2, ... in the leftmost are indices which will be useful later. Now, the actual name of the first exoplanet in our dataframe above is HD 4308 b. If there are more planets around the same star, we call them b, c, and so on in the order of discovery, not distance from the host star.

Using pandas, let's print all the columns. You can look up the meaning of each of the 80 columns [here](http://exoplanetarchive.ipac.caltech.edu/docs/API_exoplanet_columns.html). Watch out their UNITS!


```python
df.columns
```




    Index([u'pl_hostname', u'pl_letter', u'pl_discmethod', u'pl_pnum',
           u'pl_orbper', u'pl_orbpererr1', u'pl_orbpererr2', u'pl_orbperlim',
           u'pl_orbpern', u'pl_orbsmax', u'pl_orbsmaxerr1', u'pl_orbsmaxerr2',
           u'pl_orbsmaxlim', u'pl_orbsmaxn', u'pl_orbeccen', u'pl_orbeccenerr1',
           u'pl_orbeccenerr2', u'pl_orbeccenlim', u'pl_orbeccenn', u'pl_orbincl',
           u'pl_orbinclerr1', u'pl_orbinclerr2', u'pl_orbincllim', u'pl_orbincln',
           u'pl_bmassj', u'pl_bmassjerr1', u'pl_bmassjerr2', u'pl_bmassjlim',
           u'pl_bmassn', u'pl_bmassprov', u'pl_radj', u'pl_radjerr1',
           u'pl_radjerr2', u'pl_radjlim', u'pl_radn', u'pl_dens', u'pl_denserr1',
           u'pl_denserr2', u'pl_denslim', u'pl_densn', u'pl_ttvflag',
           u'pl_kepflag', u'pl_k2flag', u'ra_str', u'dec_str', u'ra', u'st_raerr',
           u'dec', u'st_decerr', u'st_posn', u'st_dist', u'st_disterr1',
           u'st_disterr2', u'st_distlim', u'st_distn', u'st_optmag',
           u'st_optmagerr', u'st_optmaglim', u'st_optmagblend', u'st_optband',
           u'st_teff', u'st_tefferr1', u'st_tefferr2', u'st_tefflim',
           u'st_teffblend', u'st_teffn', u'st_mass', u'st_masserr1',
           u'st_masserr2', u'st_masslim', u'st_massblend', u'st_massn', u'st_rad',
           u'st_raderr1', u'st_raderr2', u'st_radlim', u'st_radblend', u'st_radn',
           u'pl_nnotes', u'rowupdate'],
          dtype='object')



Another way to know the shape of our data (i.e. the number of rows and columns) is:


```python
df.shape
```




    (3414, 80)



Have you experienced working on an excel file with 3414 rows and 80 columns of data? Using python, you will realize how easy it is to work with dataset.

# Planet discovery methods

The third column of df is `pl_discmethod` which stands for exoplanet detection method. There are several methods astronomers look for exoplanets and it is enough if you know the 5 standard techniques as follows.

* Transit
* Radial Velocity (RV a.k.a Doppler)
* Imaging
* Microlensing
* Astrometry

This [wiki](https://en.wikipedia.org/wiki/Methods_of_detecting_exoplanets) does a good job explaining each of them and it is instructive for you to study them separately if you are interested to learn more on the principle behind each method.

Now, let's determine which methods are used to discover the known exoplanets in our dataset. 


```python
set(df['pl_discmethod'])
```




    {'Astrometry',
     'Eclipse Timing Variations',
     'Imaging',
     'Microlensing',
     'Orbital Brightness Modulation',
     'Pulsar Timing',
     'Pulsation Timing Variations',
     'Radial Velocity',
     'Transit',
     'Transit Timing Variations'}



The natural question to ask is:

### How many planets are discovered by each method?


```python
df['pl_discmethod'].value_counts()
```




    Transit                          2679
    Radial Velocity                   611
    Imaging                            44
    Microlensing                       43
    Transit Timing Variations          15
    Eclipse Timing Variations           8
    Orbital Brightness Modulation       6
    Pulsar Timing                       5
    Pulsation Timing Variations         2
    Astrometry                          1
    Name: pl_discmethod, dtype: int64



The code above is almost self-explanatory. We accessed the pl_discmethod column of df and use the function value_count() to count the number of occurence of the terms in each row entry. 

Now we understand that Transit and RV are currently the most prolific methods to discover exoplanets. Do you know why? That's a good research topic for those who are new to exoplanetary science. Hint: You can find out the answers [here](http://spiff.rit.edu/classes/resceu/resceu.html). 

On the other hand, Astrometry technique is still at its infancy. We expect astrometry will detect more planets with the help of [GAIA satellite](http://sci.esa.int/gaia/) to be launched in 2018.

# Histogram of exoplanet discovery


```python
filename = 'planets_raw.csv'

import pandas as pd
df = pd.read_csv(filename,delimiter=',')
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rowid</th>
      <th>pl_hostname</th>
      <th>pl_letter</th>
      <th>pl_discmethod</th>
      <th>pl_pnum</th>
      <th>pl_orbper</th>
      <th>pl_orbpererr1</th>
      <th>pl_orbpererr2</th>
      <th>pl_orbperlim</th>
      <th>pl_orbsmax</th>
      <th>...</th>
      <th>st_lumblend</th>
      <th>st_dens</th>
      <th>st_denserr1</th>
      <th>st_denserr2</th>
      <th>st_denslim</th>
      <th>st_metratio</th>
      <th>st_age</th>
      <th>st_ageerr1</th>
      <th>st_ageerr2</th>
      <th>st_agelim</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3394</td>
      <td>xi Aql</td>
      <td>b</td>
      <td>Radial Velocity</td>
      <td>1</td>
      <td>136.750000</td>
      <td>0.250000</td>
      <td>-0.250000</td>
      <td>0.0</td>
      <td>0.680000</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>[Fe/H]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3391</td>
      <td>ups And</td>
      <td>b</td>
      <td>Radial Velocity</td>
      <td>3</td>
      <td>4.617033</td>
      <td>0.000023</td>
      <td>-0.000023</td>
      <td>0.0</td>
      <td>0.059222</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3392</td>
      <td>ups And</td>
      <td>c</td>
      <td>Radial Velocity</td>
      <td>3</td>
      <td>241.258000</td>
      <td>0.064000</td>
      <td>-0.064000</td>
      <td>0.0</td>
      <td>0.827774</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3393</td>
      <td>ups And</td>
      <td>d</td>
      <td>Radial Velocity</td>
      <td>3</td>
      <td>1276.460000</td>
      <td>0.570000</td>
      <td>-0.570000</td>
      <td>0.0</td>
      <td>2.513290</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3390</td>
      <td>tau Gem</td>
      <td>b</td>
      <td>Radial Velocity</td>
      <td>1</td>
      <td>305.500000</td>
      <td>0.100000</td>
      <td>-0.100000</td>
      <td>0.0</td>
      <td>1.170000</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>[Fe/H]</td>
      <td>1.22</td>
      <td>0.76</td>
      <td>-0.76</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 94 columns</p>
</div>



Let's divide df into separate smaller dataframes based on discovery/detection method. In this tutorial, we will focus on transit and RV in the meantime.


```python
#get all rows with Transit in the pl_disc column and put it into idx1
idx1 = df['pl_discmethod'] == 'Transit'
#create a new df called df_transit and put the contents of idx1
df_transit = df[idx1]

#do the same for RV
idx2 = df['pl_discmethod'] == 'Radial Velocity'
df_RV = df[idx2]
```

Let's see if the new dataframe called df_transit contains only exoplanets discovered by transit method: 


```python
df_transit.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rowid</th>
      <th>pl_hostname</th>
      <th>pl_letter</th>
      <th>pl_discmethod</th>
      <th>pl_pnum</th>
      <th>pl_orbper</th>
      <th>pl_orbpererr1</th>
      <th>pl_orbpererr2</th>
      <th>pl_orbperlim</th>
      <th>pl_orbsmax</th>
      <th>...</th>
      <th>st_denslim</th>
      <th>st_metfe</th>
      <th>st_metfeerr1</th>
      <th>st_metfeerr2</th>
      <th>st_metfelim</th>
      <th>st_metfeblend</th>
      <th>st_age</th>
      <th>st_ageerr1</th>
      <th>st_ageerr2</th>
      <th>st_agelim</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>47</th>
      <td>48</td>
      <td>BD+20 594</td>
      <td>b</td>
      <td>Transit</td>
      <td>1</td>
      <td>41.685500</td>
      <td>0.003000</td>
      <td>-0.003100</td>
      <td>0.0</td>
      <td>0.24100</td>
      <td>...</td>
      <td>0.0</td>
      <td>-0.15</td>
      <td>0.05</td>
      <td>-0.05</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>3.34</td>
      <td>1.95</td>
      <td>-1.49</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>61</th>
      <td>62</td>
      <td>CoRoT-1</td>
      <td>b</td>
      <td>Transit</td>
      <td>1</td>
      <td>1.508956</td>
      <td>0.000006</td>
      <td>-0.000006</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>-0.30</td>
      <td>0.25</td>
      <td>-0.25</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>62</th>
      <td>63</td>
      <td>CoRoT-10</td>
      <td>b</td>
      <td>Transit</td>
      <td>1</td>
      <td>13.240600</td>
      <td>0.000200</td>
      <td>-0.000200</td>
      <td>0.0</td>
      <td>0.10550</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.26</td>
      <td>0.07</td>
      <td>-0.07</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>3.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>63</th>
      <td>64</td>
      <td>CoRoT-11</td>
      <td>b</td>
      <td>Transit</td>
      <td>1</td>
      <td>2.994330</td>
      <td>0.000011</td>
      <td>-0.000011</td>
      <td>0.0</td>
      <td>0.04360</td>
      <td>...</td>
      <td>0.0</td>
      <td>-0.03</td>
      <td>0.08</td>
      <td>-0.08</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.00</td>
      <td>1.00</td>
      <td>-1.00</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>64</th>
      <td>65</td>
      <td>CoRoT-12</td>
      <td>b</td>
      <td>Transit</td>
      <td>1</td>
      <td>2.828042</td>
      <td>0.000013</td>
      <td>-0.000013</td>
      <td>0.0</td>
      <td>0.04016</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.16</td>
      <td>0.10</td>
      <td>-0.10</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>6.30</td>
      <td>3.10</td>
      <td>-3.10</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 109 columns</p>
</div>




```python
df_RV.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rowid</th>
      <th>pl_hostname</th>
      <th>pl_letter</th>
      <th>pl_discmethod</th>
      <th>pl_pnum</th>
      <th>pl_orbper</th>
      <th>pl_orbpererr1</th>
      <th>pl_orbpererr2</th>
      <th>pl_orbperlim</th>
      <th>pl_orbsmax</th>
      <th>...</th>
      <th>st_lumblend</th>
      <th>st_dens</th>
      <th>st_denserr1</th>
      <th>st_denserr2</th>
      <th>st_denslim</th>
      <th>st_metratio</th>
      <th>st_age</th>
      <th>st_ageerr1</th>
      <th>st_ageerr2</th>
      <th>st_agelim</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3394</td>
      <td>xi Aql</td>
      <td>b</td>
      <td>Radial Velocity</td>
      <td>1</td>
      <td>136.750000</td>
      <td>0.250000</td>
      <td>-0.250000</td>
      <td>0.0</td>
      <td>0.680000</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>[Fe/H]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3391</td>
      <td>ups And</td>
      <td>b</td>
      <td>Radial Velocity</td>
      <td>3</td>
      <td>4.617033</td>
      <td>0.000023</td>
      <td>-0.000023</td>
      <td>0.0</td>
      <td>0.059222</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3392</td>
      <td>ups And</td>
      <td>c</td>
      <td>Radial Velocity</td>
      <td>3</td>
      <td>241.258000</td>
      <td>0.064000</td>
      <td>-0.064000</td>
      <td>0.0</td>
      <td>0.827774</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3393</td>
      <td>ups And</td>
      <td>d</td>
      <td>Radial Velocity</td>
      <td>3</td>
      <td>1276.460000</td>
      <td>0.570000</td>
      <td>-0.570000</td>
      <td>0.0</td>
      <td>2.513290</td>
      <td>...</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3390</td>
      <td>tau Gem</td>
      <td>b</td>
      <td>Radial Velocity</td>
      <td>1</td>
      <td>305.500000</td>
      <td>0.100000</td>
      <td>-0.100000</td>
      <td>0.0</td>
      <td>1.170000</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>[Fe/H]</td>
      <td>1.22</td>
      <td>0.76</td>
      <td>-0.76</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 94 columns</p>
</div>



Let's count the number of planets discovered per year by each technbique, first transit then RV.


```python
df_transit['pl_disc'].value_counts(sort='False')
```




    2016    1423
    2014     798
    2015      99
    2012      92
    2011      79
    2013      78
    2010      46
    2009      18
    2008      17
    2007      16
    2006       5
    2004       5
    2002       1
    Name: pl_disc, dtype: int64




```python
df_RV['pl_disc'].value_counts(sort='False')
```




    2009    72
    2015    47
    2011    47
    2010    42
    2014    41
    2008    38
    2005    35
    2012    34
    2007    34
    2013    32
    2016    30
    2002    29
    2003    22
    2006    21
    2004    18
    2000    16
    1999    13
    2001    12
    1998     6
    1996     6
    1995     1
    1989     1
    Name: pl_disc, dtype: int64



It appears that RV has fewer detected planets than Transit method but it has significantly longer history. Let's visualize these in a histogram. 


```python
#create a new 2-column dataframe
df2= pd.DataFrame(df_RV['pl_disc'].value_counts(sort=False)) 
df2['Transit'] = df_transit['pl_disc'].value_counts(sort=False)
#combine the two dataframes into 1 for easier plotting
df2.columns = ['RV','Transit']

ax = df2.sort_index(axis=0).plot.bar()
#rotate the x-axis ticks
ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
ax.set_ylim([0,800])
#the interval [1995, 2015] can't be used since it is an array of year; 0=1989 and len(df2)=2016
ax.set_xlim([1,len(df2)-1]) 
ax.set_ylabel('Count')
ax.set_xlabel('Year of discovery')
plt.show()
```


![png](output_35_0.png)


What just happened in 2014? Also you can see that the number of detected planets by Transit method (green) overtook RV (blue) around 2010. This might give an [idea](https://en.wikipedia.org/wiki/Kepler_(spacecraft) why.

# Plotting basic parameters of exoplanets detected by Transit method

Now let's plot the period of the transiting exoplanets as a function of orbital radius (a.k.a semi-major axis). In other words, we will plot the period in the y-axis and the distance of the exoplanet from its host star in the x-axis. Note that the column `pl_orbsmax` and `pl_orbper` refers to the exoplanet's orbital distance and period, respectively.


```python
import matplotlib.pyplot as pl
%matplotlib inline

#create an empty figure
fig=pl.figure()

pl.scatter(x=df_transit['pl_orbper'], y=df_transit['pl_bmassj'], color='blue')
#below is for putting the labels on x and y-axes
pl.xlabel('Orbital distance [AU]')
pl.ylabel('Orbital period [days]')
#to add title
pl.title('Transiting exoplanets')
#to reveal plot
pl.show()
```


![png](output_39_0.png)


Since we want to see datapoints, we used the `scatter` function of `pl`. The x- and y-variables as well as color are specified.

What can you tell about the plot? Describe below. Note that the unit of orbital period is **days** and that of orbital distance is **AU** (Astronomical Unit; 1 AU = Earth-Sun distance = $1.496\times10^{11}$ meters) In comparison, the orbital distance of Mercury is 0.39 AU. 



One visualization technique we can use to spread out a plot that is very crowded like shown above is to use the logarithmic plot. Remember that $\log_{10}100 = 2$. So let's try making a log-log scatter plot.  

To make it easier, let's put solar system objects as references. See the relevant values [here](http://nssdc.gsfc.nasa.gov/planetary/factsheet/). We will also convert the units from days to year.


```python
#define the masses and orbital radii of some system planets
one_year = 365.2 #days

orbper_Neptune   = 59800
orbrad_Neptune   = 30.07 #AU

orbper_Uranus    = 30589
orbrad_Uranus    = 19.19 #AU

orbper_Saturn    = 10747
orbrad_Saturn    = 9.54 #AU

orbper_Jupiter   = 4331
orbrad_Jupiter   = 5.2 #AU

orbper_Mars      = 687.0
orbrad_Mars      = 1.52 #AU

orbper_Earth     = 365.2
orbrad_Earth     = 1.0 #AU

orbper_Venus     = 224.7
orbrad_Venus     = 0.72 #AU

orbper_Mercury   = 88.0
orbrad_Mercury   = 0.39 #AU

import matplotlib.pyplot as pl
%matplotlib inline

fig = pl.figure()
#scatter plot is just a plot specified to have 'o' markers
pl.plot(df_transit['pl_orbsmax'], df_transit['pl_orbper']/one_year, 'bo', label='Transiting\nexoplanets')

#plot solar system values with labels; there is a better way to do this but suffice for now
pl.plot(orbrad_Neptune, orbper_Neptune/one_year, marker='8', color='r', label='Neptune')
pl.plot(orbrad_Uranus, orbper_Uranus/one_year, marker='x', color='r', label='Uranus')
pl.plot(orbrad_Saturn, orbper_Saturn/one_year, marker='h', color='r', label='Saturn')
pl.plot(orbrad_Jupiter, orbper_Jupiter/one_year, marker='p', color='r', label='Jupiter')

pl.plot(orbrad_Mars, orbper_Mars/one_year, marker='D', color='r', label='Mars')
pl.plot(orbrad_Earth, orbper_Earth/one_year, marker='o', color='r', label='Earth')
pl.plot(orbrad_Venus, orbper_Venus/one_year, marker='s', color='r', label='Venus')
pl.plot(orbrad_Mercury, orbper_Mercury/one_year, marker='*', color='r', label='Mercury')

#include axes with labels
pl.xlabel('Orbital distance [AU]')
pl.ylabel('Orbital period [year]')
#change to logarithmic scale
pl.xscale('log')
pl.yscale('log')
#add a translucent legend, etc.
pl.legend(loc='best', numpoints = 1, fontsize=12, handlelength=0.5, fancybox=True, framealpha=0.5)
pl.show()
```


![png](output_43_0.png)


Interesting! There are two things we can immediately say about this plot. 
* First, most of the points lie along the same line. 
* Second, most of the detected transiting exoplanets have shorter periods and smaller orbital distances than solar system planets.

Since the datapoints are almost collinear, can we say that there is a linear relationship between orbital period and orbital distance? The answer is NO. The above is a log-log plot and therefore a power relation exists between them.

In fact this relationship is so general relationship (applies to solar system bodies as well as exoplanets) that we consider this a universal law. Have you guessed which? If so, what is the value of the exponent, $x$
\begin{equation}
P \propto d^{x}
\end{equation}
where $d$ is the orbital distance and $P$ is the period?
 
It might be helpful if we fit a regression line on the log-log plot above and determine the exponent, $x$.

# Fitting a regression line

Before we can fit a regression line, we should take note that not all exoplanets have orbital period and orbital distance measurements. We can use `len` function to count the number of exoplanets which have measured values.


```python
len(df_transit['pl_orbsmax']>0) #>0 to count only non-zero values
```




    2679




```python
len(df_transit['pl_orbper']>0)
```




    2679



So they both have 2679 measurements. Does it mean that each transiting exoplanet has both measured period and orbital radius? Using the `query` will do the job. 


```python
count_both = df_transit.query('pl_orbsmax> 0 and pl_orbper>0')
len(count_both)
```




    1234



So we see that only 1234 transiting exoplanets have both measured periods and orbital radii. Let's make another dataframe called df_transit2 to be used for fitting.


```python
df_transit2= df_transit.query('pl_orbsmax> 0 and pl_orbper>0')
```

Python has a lot of libraries especially for statistics. In this case, we will use scipy that already have functions for regression called `linregress`. To seek help, try


```python
from scipy import stats

stats.linregress?
```

A screen will pop-up showing the documentation about `lingress`.


```python
from scipy import stats
import numpy as np

#convert to log first
x=np.log(df_transit2['pl_orbsmax'])
y=np.log(df_transit2['pl_orbper'])

#do the fitting
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

#print results; \t for tab, \n for new line
print('slope\t\t={0}\nintercept\t={1}\nr-value\t\t={2}\np-value\t\t={3}\nstandard error\t={4}' \
      .format(slope, intercept, r_value, p_value, std_err))
```

    slope		=1.4668272603
    intercept	=5.85692903636
    r-value		=0.991059839118
    p-value		=0.0
    standard error	=0.00562585538721


The answer we got is about **1.5** or **3/2**. In other words,

\begin{equation}
P \propto d^{3/2}
\end{equation}

Does it give you an idea now what law we are referring to? [Here's the answer](https://en.wikipedia.org/wiki/Kepler's_laws_of_planetary_motion#Third_law).

This relationship is strong since, the r-squared value:


```python
print('r-squared= {:.2f}%'.format(r_value**2*100)) # ** is for raising into power
```

    r-squared= 98.22%


Now, let's proceed to the second point that most of the detected transiting exoplanets have very short periods at small orbital distances compared to that of solar system planets. We ask, what is the size of these transiting planets much closer than Mercury? So let's plot the radius as a function orbital distance. Again, we will plot this in convenient Jupiter-radius units and year. 


```python
#define the masses and orbital radii of some system planets
one_year      = 365.2 #days

rad_Neptune   = 49.528e6 #m
orbrad_Neptune   = 30.07 #AU

rad_Uranus    = 51.118e6 #m
orbrad_Uranus    = 19.19 #AU

rad_Saturn    = 120.536e6 #m
orbrad_Saturn    = 9.54 #AU

rad_Jupiter   = 142.984e6 #m
orbrad_Jupiter   = 5.2 #AU

rad_Mars      = 6.792e6 #m
orbrad_Mars      = 1.52 #AU

rad_Earth     = 12.756e6 #m
orbrad_Earth     = 1.0 #AU

rad_Venus     = 12.104e6 #m
orbrad_Venus     = 0.72 #AU

rad_Mercury   = 4.879e6 # #m
orbrad_Mercury   = 0.39 #AU

import matplotlib.pyplot as pl
%matplotlib inline

fig = pl.figure()
#scatter plot is just a plot specified to have 'o' markers
pl.plot(df_transit['pl_orbsmax']/one_year, df_transit['pl_radj'], 'bo', label='Transiting\nexoplanets')

#plot solar system values with labels; there is a better way to do this but suffice for now
pl.plot(orbrad_Neptune/one_year, rad_Neptune/rad_Jupiter, marker='8', color='r', label='Neptune')
pl.plot(orbrad_Uranus/one_year, rad_Uranus/rad_Jupiter, marker='x', color='r', label='Uranus')
pl.plot(orbrad_Saturn/one_year, rad_Saturn/rad_Jupiter, marker='h', color='r', label='Saturn')
pl.plot(orbrad_Jupiter/one_year, rad_Jupiter/rad_Jupiter, marker='p', color='r', label='Jupiter')

pl.plot(orbrad_Mars/one_year, rad_Mars/rad_Jupiter, marker='D', color='r', label='Mars')
pl.plot(orbrad_Earth/one_year, rad_Earth/rad_Jupiter, marker='o', color='r', label='Earth')
pl.plot(orbrad_Venus/one_year, rad_Venus/rad_Jupiter, marker='s', color='r', label='Venus')
pl.plot(orbrad_Mercury/one_year, rad_Mercury/rad_Jupiter, marker='*', color='r', label='Mercury')

#include axes with labels
pl.xlabel('Orbital distance [AU]')
pl.ylabel('Planet radius [$R_{J}$]')
#change to logarithmic scale
pl.xscale('log')
pl.yscale('log')
#add a translucent legend, etc.
pl.legend(loc='best', numpoints = 1, fontsize=10, handlelength=0.5, fancybox=True, framealpha=0.5)
pl.show()
```


![png](output_61_0.png)


Now, we see that most of the transiting planets have radii comparable to that of Neptune but orbits much closer to their stars than Mercury's orbit around the Sun. This is interesting because this discovery does not resemble anything like our solar system. Immediate questions that arise are:

* How can gas giant (or terrestrial) exoplanets be so close to the star without evaporating?
* Did it form there as it is (i.e. in-situ)?
* Did it move from an initial location farther out and eventually migrated inwards?
* Also, why are there two blobs in the plot? 
* If the blob feature is real, do they correspond to two distinct exoplanet classes?
* Or perhaps this is an observational bias?


These are questions that I will leave unanswered because they are currently open problems in exoplanetary science and currently a hot topic.

# RV, Imaging, Microlensing and other techniques

Let's see how the distribution look like if we plot exoplanets based on their detection method. First, we will create new df corresponding to their techniques.  


```python
#Do the same for RV
idx2 = df['pl_discmethod'] == 'Radial Velocity'
df_RV = df[idx2]

idx3 = df['pl_discmethod'] == 'Imaging'
df_DI = df[idx3]

idx4 = df['pl_discmethod'] == 'Microlensing'
df_ML = df[idx4]

idx5 = df['pl_discmethod'] == 'Astrometry'
df_A = df[idx5]

idx6 = df['pl_discmethod'] == 'Transit Timing Variations'
df_TTV = df[idx6]

idx7 = df['pl_discmethod'] == 'Eclipse Timing Variations'
df_ETV = df[idx7]

idx8 = df['pl_discmethod'] == 'Pulsar Timing'
df_PT = df[idx8]

idx9 = df['pl_discmethod'] == 'Pulsation Timing Variations'
df_PTV = df[idx9]

idx10 = df['pl_discmethod'] == 'Orbital Brightness Modulation'
df_OBM = df[idx10]
```


```python
one_year = 365.2 #days

orbper_Neptune   = 59800
orbrad_Neptune   = 30.07 #AU

orbper_Uranus    = 30589
orbrad_Uranus    = 19.19 #AU

orbper_Saturn    = 10747
orbrad_Saturn    = 9.54 #AU

orbper_Jupiter   = 4331
orbrad_Jupiter   = 5.2 #AU

orbper_Mars      = 687.0
orbrad_Mars      = 1.52 #AU

orbper_Earth     = 365.2
orbrad_Earth     = 1.0 #AU

orbper_Venus     = 224.7
orbrad_Venus     = 0.72 #AU

orbper_Mercury   = 88.0
orbrad_Mercury   = 0.39 #AU

import matplotlib.pyplot as pl
%matplotlib inline

fig = pl.figure()
#scatter plot is just a plot specified to have 'o' markers
pl.plot(df_transit['pl_orbsmax'], df_transit['pl_orbper']/one_year, 'bo', label='Transit', alpha=0.5)
pl.plot(df_RV['pl_orbsmax'], df_RV['pl_orbper']/one_year, 'go', label='RV', alpha=0.5)
pl.plot(df_ML['pl_orbsmax'], df_ML['pl_orbper']/one_year, 'mo', label='Microlensing')
pl.plot(df_DI['pl_orbsmax'], df_DI['pl_orbper']/one_year, 'yo', label='Imaging')
pl.plot(df_TTV['pl_orbsmax'], df_TTV['pl_orbper']/one_year, 'co', label='Timing Variation')
pl.plot(df_OBM['pl_orbsmax'], df_OBM['pl_orbper']/one_year, 'ko', label='Brightness modulation')

#plot solar system values with labels; there is a better way to do this but suffice for now
pl.plot(orbrad_Neptune, orbper_Neptune/one_year, marker='8', color='r', label='Neptune')
pl.plot(orbrad_Uranus, orbper_Uranus/one_year, marker='x', color='r', label='Uranus')
pl.plot(orbrad_Saturn, orbper_Saturn/one_year, marker='h', color='r', label='Saturn')
pl.plot(orbrad_Jupiter, orbper_Jupiter/one_year, marker='p', color='r', label='Jupiter')

pl.plot(orbrad_Mars, orbper_Mars/one_year, marker='D', color='r', label='Mars')
pl.plot(orbrad_Earth, orbper_Earth/one_year, marker='o', color='r', label='Earth')
pl.plot(orbrad_Venus, orbper_Venus/one_year, marker='s', color='r', label='Venus')
pl.plot(orbrad_Mercury, orbper_Mercury/one_year, marker='*', color='r', label='Mercury')

#include axes with labels
pl.xlabel('Orbital distance [AU]')
pl.ylabel('Planet period [year]')
#change to logarithmic scale
pl.xscale('log')
pl.yscale('log')
#add a translucent legend, etc.
pl.legend(loc=2, numpoints = 1, fontsize=8, handlelength=0.5, fancybox=True, framealpha=0.5)
pl.show()
```


![png](output_65_0.png)


So the law still holds for any detected exoplanets so far (as expected). Let's see the distribution of masses as a function of orbital distance.

# Mass-orbital radius distribution


```python
#Constants that will be useful later
M_E = 5.972e24 #kg
a_E = 149.60e6 #m 
R_E = 6371e3 #km
P_E = 365 #d

M_J = 1.898e27 #kg
a_J = 778.57e6 #m
R_J = 69911e3 #m
P_J = 11.86*P_E

M_N = 1.024e26
a_N = 4495.06e6 #m
R_N = 24622e3 #m
P_N = 164.8*P_E

from matplotlib import pylab as pl
%pylab inline

pl.plot(df_transit['pl_orbsmax'],df_transit['pl_bmassj'],'bo', label='transit ({})'.format(np.count_nonzero(df_transit['pl_bmassj']>0)))
pl.plot(df_RV['pl_orbsmax'],df_RV['pl_bmassj'],'ro', label='RV ({})'.format(np.count_nonzero(df_RV['pl_bmassj']>0)))
pl.plot(df_ML['pl_orbsmax'],df_ML['pl_bmassj'],'go', label='microlensing ({})'.format(np.count_nonzero(df_ML['pl_bmassj']>0)))
pl.plot(df_DI['pl_orbsmax'],df_DI['pl_bmassj'],'mo', label='direct imaging ({})'.format(np.count_nonzero(df_DI['pl_bmassj']>0)))
pl.plot(df_TTV['pl_orbsmax'],df_TTV['pl_bmassj'],'yo', label='TTV ({})'.format(np.count_nonzero(df_TTV['pl_bmassj']>0)))
pl.plot(df_OBM['pl_orbsmax'],df_OBM['pl_bmassj'],'co', label='orb. br. mod. ({})'.format(np.count_nonzero(df_OBM['pl_bmassj']>0)))
pl.xlabel('Orbital distance [AU]')
pl.ylabel('Planet mass [$M_{J}$]')
pl.xlim([5e-3, 5e5])
pl.xscale('log')
pl.yscale('log')
pl.plot(a_E/a_E,M_E/M_J,'k*', markersize=15, label='Earth')
pl.plot(a_J/a_E,M_J/M_J,'kD', markersize=12, label='Jupiter')
pl.plot(a_N/a_E,M_N/M_J,'k^', markersize=15, label='Neptune')
pl.legend(loc=4, numpoints = 1, fontsize=10)
pl.show()
```

    Populating the interactive namespace from numpy and matplotlib



![png](output_68_1.png)


So now we can see which particular technique is effective in which regions. Direct imaging (magenta dots) is effective at finding planets faraway from their host stars while transit is effective at smaller separations. Why do you think so?

And pay attention to the region close to the balck star (i.e. Earth). Have we seen exoplanets that occupy the same region as Earth? None yet. This is the current research in exoplanets. To find and characterize Earth-like exoplanets. There are tons of reasons why this is such a technological challenge. We will probably discuss more on that on separate tutorial. 

# Exercises:
* Explore the different planet parameters such as eccentricity, inclination, effective temperature, etc. by utilizing various plots
* Explore the stellar parameters of planets such as effective spectral type, temperature, metallicity, etc.

For advanced students, we recommend trying various plots offered by the `pandas` library. An example is the following.

### Scatter-matrix


```python
from pandas.tools.plotting import scatter_matrix

scatter_matrix(df[['pl_radj', 'pl_bmassj', 'pl_orbsmax']], alpha=0.2, figsize=(6, 6), diagonal='kde');
```


![png](output_72_0.png)


Another powerful python library is called [seaborn](http://seaborn.pydata.org/). It offers more advanced plotting capabilities so be sure to learn how to use them. The following is an example.

### Pairplots
This is a powerful way to survey relationship among variables. A particular scattered pairplot implies no correlation while a distribution with a definite slope implies otherwise. Be sure to try varying the keyword parameters.


```python
import seaborn as sb

variables=df[['pl_radj', 'pl_bmassj', 'pl_dens', 'pl_orbsmax',"st_mass","st_teff","st_rad"]].dropna()
sb.pairplot(variables, diag_kind="kde", plot_kws=dict(s=50, edgecolor="b", linewidth=1), diag_kws=dict(shade=True));
#, hue="pl_discmethod", markers="+"
```


![png](output_74_0.png)



```python

```
