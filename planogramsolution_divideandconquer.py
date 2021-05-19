import numpy as np
import pandas as pd
import argparse

def knapsack_brute(shelf, products):
    W = int(shelf[1]['width'])
    N = len(products)
    
    # build a table of N+1 by W+1 where the first row is all 0
    # built a table of N+1 by W+1 where 1 represents the item in that row being picked for maximum value 
    # N is the number of products
    # W is the total width of the shelf
    K = [[0 for x in range(W + 1)] for x in range(N + 1)]
    L = [[0 for x in range(W + 1)] for x in range(N + 1)]
    
    # populate table K[][]
    for n in range(1, N+1):
        for w in range(W+1):
            # if product capcacity is less than or equals to current maximum capacity and 
            # the value of item n + calculated value from previous row and reduced capacity is greater than the value of the cell in the above row
            # set it to that value
            if products[n-1][1] <= w and (K[n-1][w] < products[n-1][2] + K[n-1][w-products[n-1][1]]):
                K[n][w] = products[n-1][2] + K[n-1][w-products[n-1][1]]
                L[n][w] = 1
            # if the addition of the new value doe not increase the value more than in the previous row
            # set it the value of the above row
            else:
                K[n][w] = K[n-1][w]
                L[n][w] = 0
    """
    for w in K:
        print(w)
    print("")
    for w in L:
        print(w)
    """
    # create list sqeuence of numbers that tracks whether the product was picked with n=1 at the start
    # create list of products added in the optimal solution
    # remove them from products and return products
    # sum up the total width of product son the shelf
    optimal_products_bin = []
    w = W
    for n in range(N,0,-1):
        if L[n][w]==1:
            w = w - products[n-1][1]
            optimal_products_bin.insert(0,1)
        else:
            optimal_products_bin.insert(0,0)
            
    new_products = []
    placed_products = []
    shelf_width = 0
    for i in range(len(optimal_products_bin)):
        if (optimal_products_bin[i]) == 0:
            new_products.append(products[i])
        elif(optimal_products_bin[i]) == 1:
            placed_products.append(products[i][0])
            shelf_width += products[i][1]
    #print(new_products)
        
    return K[N][W],new_products, placed_products, shelf_width


def planogram_divideandconquer(fixture, products):
    
    fixture = fixture.values.tolist()
    products = products.values.tolist()
    
    shelf_to_product = []
    for f in fixture:
        shelf_to_product.append([f[0],{'product_id':[], 'width':f[2], 'profit': 0}])
    
    # in order of fixtures, find the optimal solution for each one with brute force
    for i in range(len(shelf_to_product)):
        shelf = shelf_to_product[i]
        shelf_value, products, placed_products, shelf_width = knapsack_brute(shelf, products)
        shelf_to_product[i][1]['product_id'] = placed_products
        shelf_to_product[i][1]['profit'] = shelf_value
        shelf_to_product[i][1]['product_width_mm'] = shelf_width 
        
    # convert to a dataframe
    for i in range(len(shelf_to_product)):
        x = shelf_to_product[i][1]
        x['shelf_no'] = shelf_to_product[i][0]
        x['shelf_width_cm'] = fixture[i][1]
        x['n_items'] = len(x['product_id'])
        
        shelf_to_product[i] = x
    return pd.DataFrame(shelf_to_product)[['shelf_no','shelf_width_cm','product_id','n_items','product_width_mm','profit']]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--products",
        type=argparse.FileType(mode="r"),
        default="products.csv",
        help="products input file"
    )
    parser.add_argument(
        "--fixture",
        type=argparse.FileType(mode="r"),
        default="fixture.csv",
        help="fixture input file"
    )
    parser.add_argument(
        "--out", "-o", default="solution_divideandconquer.csv", help="solution output file"
    )

    args = parser.parse_args()

    fixture = pd.read_csv(args.fixture)
    products = pd.read_csv(args.products)

    #alterations to the dataframe arguments
    products = pd.read_csv('products.csv')
    fixture = pd.read_csv('fixture.csv')
    fixture['shelf_width_mm'] = fixture['shelf_width_cm'] * 10
    fixture['profit'] = 0
    fixture

    solution = planogram_divideandconquer(fixture, products)
    
    solution.to_csv(args.out, index=False)
    print('open csv file to see entire solution')
    print("stats:", solution)
