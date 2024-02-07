"""
Compute Sales

This program computes the total price of the items from two
JSON files: one for the products information and the other
for the sales information

Author:
    Julia Gabriela Pinedo (A01795315)
"""
import json
import sys
import time


class ComputeSales:
    """
    Class to compute the sales of some products
    """

    def __init__(self, file_1, file_2):
        """
        Initializes the ComputeSales object

        Returns:
            None
        """
        self.file_path_1 = file_1
        self.file_path_2 = file_2

    def process_json_files(self):
        """
        This function processes the JSON files and inputs them
        into the 'compute_sales' function

        Returns:
            None
        """
        try:
            product_info = self.read_json_file(self.file_path_1)
            sales_info = self.read_json_file(self.file_path_2)

            if product_info and sales_info:
                self.compute_sales(product_info, sales_info)

        except FileNotFoundError as e:
            if not (self.file_path_1 and self.file_path_2):
                print('Files are not found')
            else:
                print(f'File not found: {e.filename}')

    @staticmethod
    def read_json_file(file_path):
        """
        This function reads any JSON file and returns a dictionary
        with the data from the file

        Args:
            file_path (str): The JSON file path

        Returns:
            A dictionary with the data from the JSON file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError as e:
            print(f'File not found: {e.filename}')
            return None

    @staticmethod
    def save_product_prices(prod_dict, product_key='title', price_key='price'):
        """
        This function populates a dictionary with the products and their
        associated prices

        Args:
            prod_dict (dict): A dictionary containing the products and
            their information
            product_key (str): The name of the key that contains the name of
            the product (default: 'title')
            price_key (str): The name of the key that contains the price of
            the product (default: 'price')

        Returns:
            dict: A dictionary with the products and their prices
        """
        product_prices = {}
        for product in prod_dict:
            product_prices[product[product_key]] = product[price_key]
        return product_prices

    @staticmethod
    def calculate_total_price(prices_dict, sales_dict, product_key='Product',
                              quantity_key='Quantity'):
        """
        This function calculates the total price of the products and their
        associated prices

        Args:
            prices_dict (dict): A dictionary with the products and
            their prices
            sales_dict (dict): A dictionary with the sales information
            product_key (str): The name of the key that contains the name of
            the product (default: 'Product')
            quantity_key (str): The name of the key that contains the quantity
            of the product (default: 'Quantity')

        Returns:
            total_price (float): The total price of the products
        """
        total_price = 0
        for sale in sales_dict:
            product_title = sale[product_key]
            quantity = sale[quantity_key]
            # Extra code: Handling negative quantity values in input files
            if quantity < 0:
                print(f'Error: Negative quantity for product "{product_title}". '
                      f'Skipping this value...')
                continue
            if product_title in prices_dict:
                # Extra code: These functions prints the price per product
                # individually to handle unexpected errors
                price_per_sale = prices_dict[product_title]
                price_per_qty = quantity * price_per_sale
                total_price += price_per_qty
                print(f'Product: {product_title}, '
                      f'Qty: {quantity}, Price: ${price_per_qty:.2f}')
            else:
                print(f'Error: The product "{product_title}" was not found '
                      f'in the price catalogue')
        return total_price

    def compute_sales(self, product_info, sales_info):
        """
        This function computes the total price per sale of the products

        Args:
            product_info (dict): A dictionary with the products information
            sales_info (dict): A dictionary with the sales information for
            each product

        Returns:
            float: The total price of the products
        """
        start_time = time.time()

        prices_dictionary = self.save_product_prices(product_info)
        total_price = self.calculate_total_price(prices_dictionary, sales_info)

        end_time = time.time()

        print(f'\nTotal Price: ${total_price:.2f}')
        print(f'\nElapsed Time: {end_time - start_time} s')

        with open('SalesResults.txt', 'w', encoding='utf-8') as file:
            file.write(f'Total Price: ${total_price:.2f}')
            file.write(f'\nElapsed Time: {end_time - start_time} s')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python3 compute_sales.py <file_path_1> <file_path_2>')
    else:
        file_path_1 = sys.argv[1]
        file_path_2 = sys.argv[2]
        data_processor = ComputeSales(file_path_1, file_path_2)
        data_processor.process_json_files()
