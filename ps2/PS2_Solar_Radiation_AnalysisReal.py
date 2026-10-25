#these are important modules for diz
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance


#loading the data
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)


folder = Path(__file__).parent
df = pd.read_csv(folder / 'SolarPrediction.csv')

fig_folder = folder / 'figures'
fig_folder.mkdir(exist_ok=True)

def save_and_show(name):
    plt.savefig(fig_folder / name, dpi=150, bbox_inches='tight')
    plt.show()
    plt.close('all')
#every plot gets saved into figures/ so the pngs always match this code
#closing after each plot stops the next plot (eg pandas .plot) drawing on top of the old one

print("=" * 60)
print("LOADING THE DATA")
print("=" * 60)

print(f"\nRows: {df.shape[0]}   Columns: {df.shape[1]}")

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values per column:")
print(df.isnull().sum()) #chking all the missing values before

print("\nSummary statistics:")
print(df.describe().round(2))



df['Date'] = pd.to_datetime(df['Data'].str.split(' ').str[0], format='%m/%d/%Y')
# take only the date part to get another data row that will be useful for chking which date got max radiation

date_str = df['Date'].dt.strftime('%Y-%m-%d')
df['DateTime'] = pd.to_datetime(date_str + ' ' + df['Time'])
df['SunRise'] = pd.to_datetime(date_str + ' ' + df['TimeSunRise'])
df['SunSet'] = pd.to_datetime(date_str + ' ' + df['TimeSunSet'])

df = df.rename(columns={'WindDirection(Degrees)': 'WindDirection', 'Speed': 'WindSpeed'})
# shorter column names

df = df.sort_values('DateTime').reset_index(drop=True)
# the csv is not in time order

df['Hour'] = df['DateTime'].dt.hour
df['IsDay'] = (df['DateTime'] >= df['SunRise']) & (df['DateTime'] <= df['SunSet'])
# extra columns used later

print("\n" + "=" * 60)
print("PREPARED DATA")
print("=" * 60)

print("\nNew columns (first 5 rows):")
print(df[['DateTime', 'Radiation', 'SunRise', 'SunSet', 'IsDay']].head())
#PREPARING THE DATA IS IMPORTANT


per_day = df.groupby('Date').size()

print("\nReadings per day:")
print(per_day.describe().round(1))

print("\nDays with the fewest readings:")
print(per_day.sort_values().head())
#to check how complete a day is.... if we dont have values of night readings... this will increase the average of that day.(which is error)


#NOW LETS VISUALIZE PART A

print("\n" + "=" * 60)
print("PART A - DATA VISUALISATION")
print("=" * 60)


timeline = df.set_index('DateTime')['Radiation'].resample('5min').mean()

plt.figure(figsize=(14, 4))
plt.plot(timeline.index, timeline.values, linewidth=0.3)
plt.title('Solar Radiation Sep - Dec 2016')
plt.xlabel('Date')
plt.ylabel('Radiation (W/m2)')
save_and_show('A1_radiation_timeseries.png')
#Radiation over time.


df.boxplot(column='Radiation', by='Hour', figsize=(12, 5))
plt.title('Radiation by hour of day')
plt.suptitle('')
plt.xlabel('Hour')
plt.ylabel('Radiation (W/m2)')
save_and_show('A2_radiation_by_hour_boxplot.png')
#Radiation over Hour...


cols = ['Temperature', 'Humidity', 'Pressure', 'WindSpeed']
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

for ax, c in zip(axes.flatten(), cols):
    ax.scatter(df[c], df['Radiation'], s=2, alpha=0.2)
    ax.set_xlabel(c)
    ax.set_ylabel('Radiation')
    ax.set_title(f'Radiation vs {c}')

plt.tight_layout()
save_and_show('A3_radiation_vs_parameters.png')
#this is radiation against other parameters


num_cols = ['Radiation', 'Temperature', 'Humidity', 'Pressure', 'WindDirection', 'WindSpeed']
corr = df[num_cols].corr()

print("\nCorrelation matrix:")
print(corr.round(2))

plt.figure(figsize=(7, 6))
plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar()
plt.xticks(range(len(num_cols)), num_cols, rotation=45)
plt.yticks(range(len(num_cols)), num_cols)

for i in range(len(num_cols)):
    for j in range(len(num_cols)):
        plt.text(j, i, round(corr.iloc[i, j], 2), ha='center', va='center')

plt.title('Correlation matrix')
save_and_show('A4_correlation_heatmap.png')
#correlation heatmap GOES from -1 to 1... 


plt.hist(df['Humidity'], bins=50)
plt.title('Humidity distribution')
plt.xlabel('Humidity (%)')
plt.ylabel('Count')
save_and_show('A5_humidity_distribution.png')

print("\nOutlier counts:")
print(f"  Humidity > 100         : {(df['Humidity'] > 100).sum()}")
print(f"  Radiation > 1361       : {(df['Radiation'] > 1361).sum()}")
print(f"  Min radiation at night : {df.loc[~df['IsDay'], 'Radiation'].min()} W/m2")

#THESE ARE OUTLIER CASES THAT Actualy is not possible... you cannot have humidity > 100 and radiation>1361(1361 is solar constant and that should be very hard to  reach)


df['Month'] = df['DateTime'].dt.month_name()
monthly = df.pivot_table(index='Hour', columns='Month', values='Radiation', aggfunc='mean')
monthly = monthly[['September', 'October', 'November', 'December']]

print("\n--- Bonus: monthly daily cycle ---\n")
print(f"  {'Month':<12}{'Peak hour mean':>16}{'Daily mean':>12}")
for m in monthly.columns:
    print(f"  {m:<12}{monthly[m].max():>16.0f}{monthly[m].mean():>12.0f}")

monthly.plot(figsize=(12, 5), marker='o')
plt.title('Bonus: average radiation by hour for each month')
plt.xlabel('Hour of day')
plt.ylabel('Mean radiation (W/m2)')
plt.xticks(range(24))
plt.grid(alpha=0.3)
save_and_show('A6_bonus_monthly_daily_cycle.png')


#Now part B what can we inference from this data

print("\n" + "=" * 60)
print("PART B - DRAWING INFERENCES")
print("=" * 60)


print("\n--- B1. When is radiation highest? ---")

hourly = df.groupby('Hour')['Radiation'].mean() #-this is to check mean rad of each hr...(we get mean of all rad wrt the minutes)

print("\nMean radiation by hour:")
print(hourly.round(0))
print(f"\nBest hour : {hourly.idxmax()}:00  (mean {round(hourly.max())} W/m2)")

idx = df.groupby('Date')['Radiation'].idxmax()
peaks = df.loc[idx]
peak_hour = peaks['DateTime'].dt.hour + peaks['DateTime'].dt.minute / 60

print(f"Median peak time (hours)       : {round(peak_hour.median(), 2)}")
print(f"Days peaking between 11 and 13 : {round(peak_hour.between(11, 13).mean() * 100)} %")
#the above code is to check the max radiation and time of each day..


print("\n--- B2. Which parameter is related to radiation the most? ---")

params = ['Temperature', 'Humidity', 'Pressure', 'WindDirection', 'WindSpeed']

print("\nCorrelation with radiation (all readings):")
print(df[params].corrwith(df['Radiation']).sort_values().round(3))

day = df[df['IsDay']]

print("\nCorrelation with radiation (daytime only):")
print(day[params].corrwith(day['Radiation']).sort_values().round(3))
#basically there is a fnc that checks corr of parameters like temp humidity etc with radiation... and sorts the corr values in ascnding order from neg to pos


print("\n--- B3. Radiation, temperature and humidity patterns ---")

profile = df.groupby('Hour')[['Radiation', 'Temperature', 'Humidity']].mean()

print("\nHourly averages:")
print(profile.round(1))

noon = df[df['Hour'].between(11, 12)]
bright = noon[noon['Radiation'] >= 800]
dim = noon[noon['Radiation'] < 200]

print("\nNoon readings (11:00 - 13:00), medians:")
print(f"  Bright (>= 800) : humidity {bright['Humidity'].median()} %   temp {bright['Temperature'].median()} F")
print(f"  Dim    (< 200)  : humidity {dim['Humidity'].median()} %   temp {dim['Temperature'].median()} F")
#this is a cool observation... in profile dataframe we see that radiation peeks at 12 but temp stays hgih until 13-14 due to "THERMAL LAG".... cuz ground keeps releasing heat.
#and in the same hr betweeen the minutes... we see difference in bright and dim readings that shows how cloud effects reading


print("\n--- B4. Unusual observations ---\n")

print(f"  Noon readings below 200 : {(noon['Radiation'] < 200).sum()}")
print(f"  Wind > 25 mph           : {(df['WindSpeed'] > 25).sum()}   (max {df['WindSpeed'].max()} mph)")
#TO check Outliers... basically in middy rad should be high arnd 700+ but reading shows 200.. this shows cloud blocking sunrays from sensor..
# winds are usually 5-6 mph lekin 25 is unusual.. so we count the columns with unsual windspeeds


print("\n--- B5. Bonus insight: the highest peak is NOT the sunniest day ---\n")

day_stats = df.groupby('Date')['Radiation'].agg(['max', 'mean'])
top_day = day_stats['max'].idxmax()
rank = int(day_stats['mean'].rank(ascending=False)[top_day])

print(f"  Day with the highest peak  : {top_day.date()}  (peak {day_stats.loc[top_day, 'max']:.0f} W/m2)")
print(f"  Its average radiation      : {day_stats.loc[top_day, 'mean']:.0f} W/m2")
print(f"  Average of a typical day   : {day_stats['mean'].median():.0f} W/m2")
print(f"  Rank by average            : {rank} out of {len(day_stats)} days")
print(f"  Correlation of daily max vs daily average : {day_stats['max'].corr(day_stats['mean']):.2f}")

plt.figure(figsize=(7, 5))
plt.scatter(day_stats['mean'], day_stats['max'], alpha=0.6)
plt.scatter(day_stats.loc[top_day, 'mean'], day_stats.loc[top_day, 'max'], color='red', s=80,
            label=f'{top_day.date()} (highest peak)')
plt.xlabel('Daily average radiation (W/m2)')
plt.ylabel('Daily maximum radiation (W/m2)')
plt.title('Each dot is one day: a high peak does not mean a sunny day')
plt.legend()
save_and_show('B5_bonus_daily_max_vs_mean.png')


#PartC ... daywise report for radiation

print("\n" + "=" * 60)
print("PART C - SOLAR DAY ANALYSIS")
print("=" * 60)


idx = df.groupby('Date')['Radiation'].idxmax()
peaks = df.loc[idx].set_index('Date')

daily = df.groupby('Date').agg(
    Readings=('Radiation', 'count'),
    MaxRadiation=('Radiation', 'max'),
    MeanRadiation=('Radiation', 'mean'),
)
daily['PeakTime'] = peaks['DateTime'].dt.time
daily['PeakAfterSunrise'] = peaks['DateTime'] - peaks['SunRise']
daily['PeakBeforeSunset'] = peaks['SunSet'] - peaks['DateTime']

print("\nDay-wise report (first 10 days):")
print(daily.head(10).round(2))

daily.to_csv(folder / 'daily_report.csv')
print("\nSaved full report to daily_report.csv")


best = daily['MaxRadiation'].idxmax()
r = peaks.loc[best]

print("\n--- Day with the highest radiation ---\n")
print(f"  Best day           : {best.date()}")
print(f"  Time               : {r['DateTime'].time()}")
print(f"  Radiation          : {r['Radiation']} W/m2")
print(f"  Temperature        : {r['Temperature']} F")
print(f"  Humidity           : {r['Humidity']} %")
print(f"  Wind speed         : {r['WindSpeed']} mph")
print(f"  Sunrise            : {r['SunRise'].time()}")
print(f"  Sunset             : {r['SunSet'].time()}")
print(f"  Peak after sunrise : {r['DateTime'] - r['SunRise']}")
print(f"  Peak before sunset : {r['SunSet'] - r['DateTime']}")
#day with highest radiation and conditions at the peak


one_day = df[df['Date'] == best]

plt.figure(figsize=(12, 4))
plt.plot(one_day['DateTime'], one_day['Radiation'])
plt.axvline(r['SunRise'], color='orange', linestyle='--', label='Sunrise')
plt.axvline(r['SunSet'], color='red', linestyle='--', label='Sunset')
plt.legend()
plt.title(f'Radiation on {best.date()}')
save_and_show('C5_peak_day_profile.png')
#we plot the values at the day with the high radiation values


top5 = daily.sort_values('MeanRadiation', ascending=False).head(5)

print("\n--- Top 5 days by average radiation ---\n")
print(top5[['MeanRadiation', 'MaxRadiation', 'Readings']].round(2))
#these 2 lines of code shows the top 5 days with higher radiation reading. a full day has 288 readings (1 reading every 5min = 24 hours)
#days with missing night readings would get an inflated average, but all top 5 days have 275+ readings so their average is fine

#BONUS TIME
print("\n" + "=" * 60)
print("BONUS - PREDICTING SOLAR RADIATION")
print("=" * 60)

frac = (df['DateTime'] - df['SunRise']) / (df['SunSet'] - df['SunRise'])
df['SunPos'] = np.where(df['IsDay'], np.sin(np.pi * frac), 0)
#where is the sun wrt sunrise and sunset...

hours = df['Hour'] + df['DateTime'].dt.minute / 60
df['TimeSin'] = np.sin(2 * np.pi * hours / 24)
df['TimeCos'] = np.cos(2 * np.pi * hours / 24)
df['DayLength'] = (df['SunSet'] - df['SunRise']).dt.total_seconds() / 3600
df['DayOfYear'] = df['DateTime'].dt.dayofyear


features = ['Temperature', 'Humidity', 'Pressure', 'WindSpeed',
            'SunPos', 'TimeSin', 'TimeCos', 'DayLength', 'DayOfYear']
X = df[features]
y = df['Radiation']
#above code is for preparing clues for training the model... we have created sunpos, time ,daylength and day of year to train the model on finer details

split = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(split.split(X, y, groups=df['Date']))
#the above 2 lines is the training data- 
#we took 94 days for training and 24 days for testing(hidden)

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]


model = HistGradientBoostingRegressor(max_iter=600, learning_rate=0.03, max_leaf_nodes=31,
                                      min_samples_leaf=40, l2_regularization=1.0, random_state=42)
model.fit(X_train, y_train)
#why this model... well we tried 8 models and got this as the best one...
pred = np.clip(model.predict(X_test), 0, None)#tests on hidden days here
 
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)
#these are prediction values

print(f"\nTrained on {len(X_train)} readings, tested on {len(X_test)} readings from unseen days\n")
print(f"  RMSE : {rmse:.1f} W/m2")
print(f"  R2   : {r2:.3f}")


plt.figure(figsize=(6, 6))
plt.scatter(y_test, pred, s=2, alpha=0.3)
plt.plot([0, 1600], [0, 1600], color='red', label='Perfect prediction')
plt.xlabel('Actual radiation (W/m2)')
plt.ylabel('Predicted radiation (W/m2)')
plt.title(f'Predicted vs actual (R2 = {r2:.3f})')
plt.legend()
save_and_show('ML2_predicted_vs_actual.png')
#plotting prediction vs actual

test = df.iloc[test_idx].copy()
test['Predicted'] = pred
one = test[test['Date'] == '2016-11-10']

plt.figure(figsize=(12, 4))
plt.plot(one['DateTime'], one['Radiation'], label='Actual')
plt.plot(one['DateTime'], one['Predicted'], label='Predicted')
plt.ylabel('Radiation (W/m2)')
plt.title('Actual vs predicted on 10 Nov 2016 (a day the model never saw)')
plt.legend()
save_and_show('ML3_test_day_profile.png')
#plotting for hidden day using our model

print("\n--- Which features are useful? ---\n")

imp = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
importance = pd.Series(imp.importances_mean, index=features).sort_values()

print(importance.sort_values(ascending=False).round(3))

importance.plot(kind='barh', figsize=(8, 5))
plt.title('Feature importance (drop in R2 when the feature is shuffled)')
plt.xlabel('Drop in R2')
save_and_show('ML1_feature_importance.png')
#Basic structure for this is shuffle test... so we scramble the column and test how worse the model getsb... 
#big drop in r2 implies that the model relied on the feature
#no drop means the feature was useless