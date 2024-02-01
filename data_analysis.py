import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('lease_price_20240201004538.csv')

def generate_histogram(df, column_name):
    plt.hist(df[column_name], bins=100, color='blue')
    plt.title(column_name)
    plt.xlabel(column_name)
    plt.ylabel("Frequency")
    plt.show()

def get_average(df, column_name):
    return format(round(df[column_name].mean(), 2), ",")

def get_median(df, column_name):
    return df[column_name].median()

def get_average_by_district(df, column_name):
    return df.groupby("District Area")[column_name].mean()

def get_standard_deviation(df, column_name):
    return round(df[column_name].std(), 4)

def get_highest(df, column_name):
    return format(df[column_name].max(), ",")

def get_lowest(df, column_name):
    return format(df[column_name].min(), ",")


if __name__ == "__main__":

    '''Generate index.md file'''
    with open("docs\index.md", "w") as file:
        file.write("# Data Analysis of Lease Price in Hong Kong\n")
        file.write("## Summary of the data\n")
        file.write(f"Number of records: **{len(df)}**\n\n")
        file.write(f"Number of district areas: **{len(df['District Area'].unique())}**\n\n")
        file.write("Data is obtained from [https://www.28hse.com/en/rent/residential](https://www.28hse.com/en/rent/residential)\n\n")
        file.write(f"Source code can be found at [https://github.com/kuanjiahong/hk-property-analysis](https://github.com/kuanjiahong/hk-property-analysis)\n\n")
        file.write("\n")

        file.write("## Lease Price\n")
        file.write(f"Highest lease price: **HKD${get_highest(df, 'Lease Price')}**\n\n")
        file.write(f"Most expensive lease price is located at **{df.loc[df['Lease Price'].idxmax()]['District Area']}** with lease price of **HKD${get_highest(df, 'Lease Price')}**\n\n")
        file.write(f"Cheapest lease price: **HKD${get_lowest(df, 'Lease Price')}**\n\n")
        file.write(f"Cheapest lease price is located at **{df.loc[df['Lease Price'].idxmin()]['District Area']}** with lease price of **HKD${get_lowest(df, 'Lease Price')}**\n\n")
        file.write(f"Average lease price: **HKD${get_average(df, 'Lease Price')}**\n\n")
        file.write(f"Median lease price: **HKD${get_median(df, 'Lease Price')}**\n\n")
        file.write(f"Standard deviation of lease price: **HKD${get_standard_deviation(df, 'Lease Price')}**\n\n")
        file.write("\n")

        file.write("## Gross Area\n")
        file.write(f"Largest gross area in sqft: **{get_highest(df, 'Gross Area')}**\n\n")
        file.write(f"Largest gross area is located at **{df.loc[df['Gross Area'].idxmax()]['District Area']}** with gross area of **{get_highest(df, 'Gross Area')}**\n\n")
        file.write(f"Smallest gross area in sqft: **{get_lowest(df, 'Gross Area')}**\n\n")
        file.write(f"Smallest gross area is located at **{df.loc[df['Gross Area'].idxmin()]['District Area']}** with gross area of **{get_lowest(df, 'Gross Area')}**\n\n")
        file.write(f"Average gross area in sqft: **{get_average(df, 'Gross Area')}**\n\n")
        file.write(f"Median gross area in sqft: **{get_median(df, 'Gross Area')}**\n\n")
        file.write(f"Standard deviation of gross area in sqft: **{get_standard_deviation(df, 'Gross Area')}**\n\n")
        file.write("\n")

        file.write("## Saleable Area\n")
        file.write(f"Largest saleable area in sqft: **{get_highest(df, 'Saleable Area')}**\n\n")
        file.write(f"Largest saleable area is located at **{df.loc[df['Saleable Area'].idxmax()]['District Area']}** with saleable area of **{get_highest(df, 'Saleable Area')}**\n\n")
        file.write(f"Smallest saleable area in sqft: **{get_lowest(df, 'Saleable Area')}**\n\n")
        file.write(f"Smallest saleable area is located at **{df.loc[df['Saleable Area'].idxmin()]['District Area']}** with saleable area of **{get_lowest(df, 'Saleable Area')}**\n\n")
        file.write(f"Average saleable area in sqft: **{get_average(df, 'Saleable Area')}**\n\n")
        file.write(f"Median saleable area in sqft: **{get_median(df, 'Saleable Area')}**\n\n")
        file.write(f"Standard deviation of saleable area in sqft: **{get_standard_deviation(df, 'Saleable Area')}**\n\n")
        file.write("\n")

        file.write("## Top 10 most expensive district areas ranked according to the district area's average price\n")
        result = df.groupby("District Area")["Lease Price"].mean().sort_values(ascending=False).head(10)
        count = 1
        for index, value in result.items():
            file.write(f"{count}. {index} : {format(round(value,2), ',')}\n")
            count += 1

        file.write("\n")

        file.write("## Top 10 cheapest district areas ranked according to district area's average price\n")
        result = df.groupby("District Area")["Lease Price"].mean().sort_values(ascending=True).head(10)
        count = 1
        for index, value in result.items():
            file.write(f"{count}. {index} : {format(round(value,2), ',')}\n")
            count += 1
        file.write("\n")

        file.write("## District Areas and their number of listings\n")
        result = df["District Area"].value_counts()
        count = 1
        for index, value in result.items():
            file.write(f"{count}. {index} : {value}\n")
            count += 1
        
        file.write("\n")


    # generate_histogram(df, "Lease Price")
    # generate_histogram(df, "Saleable Area")
    # generate_histogram(df, "Gross Area")