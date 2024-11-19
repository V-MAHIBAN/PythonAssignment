import pandas as pd
import matplotlib.pyplot as plt
import argparse


class SalesData:
    def __init__(self, file_path="sales_data.csv"):
        """
        Initializes the SalesData class by loading sales data from a CSV file.
        """
        try:
            self.df = pd.read_csv(file_path, parse_dates=["Date"])
        except FileNotFoundError:
            print("Error: Sales data file not found. Please provide a valid path.")
            self.df = pd.DataFrame()  # Empty DataFrame if file is not found

    def get_data(self):
        """
        Returns the sales data as a Pandas DataFrame.
        """
        return self.df

    def add_data(self, new_data):
        """
        Appends new sales data to the existing DataFrame.
        """
        self.df = self.df.append(new_data, ignore_index=True)

    def save_data(self, file_path="sales_data.csv"):
        """
        Saves the updated sales data to a CSV file.
        """
        self.df.to_csv(file_path, index=False)


class MonthlySalesAnalysis:
    def __init__(self, sales_data):
        self.sales_data = sales_data

    def analyze_monthly_sales(self, branch_name=None):
        """
        Analyzes monthly sales for a specific branch or all branches.
        """
        df = self.sales_data.get_data()
        if branch_name:
            df = df[df["Branch"] == branch_name]
        monthly_sales = df.groupby(pd.Grouper(key='Date', freq='M'))["Total Amount"].sum()
        return monthly_sales

    def print_monthly_sales(self, branch_name=None):
        """
        Prints and plots a formatted summary of monthly sales.
        """
        monthly_sales = self.analyze_monthly_sales(branch_name)
        print(f"Monthly Sales {'(All Branches)' if branch_name is None else f'({branch_name})'}:")
        print(monthly_sales)
        monthly_sales.plot(kind='bar', title='Monthly Sales')
        plt.xlabel('Month')
        plt.ylabel('Total Amount')
        plt.show()


class PriceAnalysis:
    def __init__(self, sales_data):
        self.sales_data = sales_data

    def analyze_product_prices(self, product_name):
        """
        Analyzes price changes for a specific product.
        """
        df = self.sales_data.get_data()
        product_df = df[df["Product"] == product_name]
        return product_df[["Date", "Price"]]

    def print_price_analysis(self, product_name):
        """
        Prints and plots a formatted summary of product price changes.
        """
        price_changes = self.analyze_product_prices(product_name)
        print(f"Price Analysis for {product_name}:")
        print(price_changes)
        price_changes.plot(x='Date', y='Price', kind='line', title=f'Price Changes for {product_name}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()


class WeeklySalesAnalysis:
    def __init__(self, sales_data):
        self.sales_data = sales_data

    def analyze_weekly_sales(self):
        """
        Analyzes weekly sales for the entire supermarket network.
        """
        df = self.sales_data.get_data()
        weekly_sales = df.groupby(pd.Grouper(key='Date', freq='W'))["Total Amount"].sum()
        return weekly_sales

    def print_weekly_sales(self):
        """
        Prints and plots a formatted summary of weekly sales.
        """
        weekly_sales = self.analyze_weekly_sales()
        print("Weekly Sales (All Branches):")
        print(weekly_sales)
        weekly_sales.plot(kind='line', title='Weekly Sales')
        plt.xlabel('Week')
        plt.ylabel('Total Amount')
        plt.show()


class ProductPreferenceAnalysis:
    def __init__(self, sales_data):
        self.sales_data = sales_data

    def analyze_product_preferences(self):
        """
        Analyzes product preferences based on sales quantity.
        """
        df = self.sales_data.get_data()
        product_preferences = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
        return product_preferences

    def print_product_preferences(self):
        """
        Prints and plots a formatted summary of product preferences.
        """
        product_preferences = self.analyze_product_preferences()
        print("Product Preferences (Top Sellers):")
        print(product_preferences)
        product_preferences.plot(kind='bar', title='Product Preferences')
        plt.xlabel('Product')
        plt.ylabel('Total Quantity Sold')
        plt.show()


class SalesDistributionAnalysis:
    def __init__(self, sales_data):
        self.sales_data = sales_data

    def analyze_sales_distribution(self, bins=10):
        """
        Analyzes the distribution of total sales amounts.
        """
        df = self.sales_data.get_data()
        sales_distribution = pd.cut(df["Total Amount"], bins=bins)
        return sales_distribution.value_counts().sort_index()

    def print_sales_distribution(self, bins=10):
        """
        Prints and plots a formatted summary of the sales amount distribution.
        """
        sales_distribution = self.analyze_sales_distribution(bins)
        print("Sales Amount Distribution:")
        print(sales_distribution)
        sales_distribution.plot(kind='bar', title='Sales Amount Distribution')
        plt.xlabel('Amount Range')
        plt.ylabel('Frequency')
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Sales Data Analysis System")
    parser.add_argument("file_path", type=str, help="Path to the CSV file containing sales data")
    args = parser.parse_args()

    sales_data = SalesData(args.file_path)

    while True:
        print("\nSelect an analysis option:")
        print("1. Monthly Sales Analysis")
        print("2. Price Analysis")
        print("3. Weekly Sales Analysis")
        print("4. Product Preference Analysis")
        print("5. Sales Distribution Analysis")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            branch_name = input("Enter branch name (or leave blank for all branches): ")
            MonthlySalesAnalysis(sales_data).print_monthly_sales(branch_name)
        elif choice == "2":
            product_name = input("Enter product name: ")
            PriceAnalysis(sales_data).print_price_analysis(product_name)
        elif choice == "3":
            WeeklySalesAnalysis(sales_data).print_weekly_sales()
        elif choice == "4":
            ProductPreferenceAnalysis(sales_data).print_product_preferences()
        elif choice == "5":
            bins = int(input("Enter number of bins for sales distribution analysis (default 10): ") or 10)
            SalesDistributionAnalysis(sales_data).print_sales_distribution(bins)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
