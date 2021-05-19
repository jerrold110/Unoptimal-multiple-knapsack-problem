import numpy as np
import pandas as pd
import argparse

def planogram_greedy(fixture, products):
    # products are sorted by profit to width ratio
    
    fixture_col = fixture.columns
    products_col = products.columns
    
    fixture = fixture.values.tolist()
    products = products.values.tolist()
    
    # dictionary of shelves and the products on them
    shelf_to_product = []
    for i in fixture:
        shelf_to_product.append({'shelf_no':i[0], 'shelf_width_cm ':i[1], 'product_id':[], 'profit':0, 'product_width_mm':0})
    # try and fit every item into each fixture until there is no more space
    # before fitting an item into a shelf, 
    for p in products:
        for f in fixture:
            if f[2]>=p[1]:
                # subtract width from fixture
                f[2] -= p[1]
                # add profit to fixture
                f[3] += p[2]
                # add record to dictionary
                shelf_to_product[int(f[0])-1]['product_id'].append(p[0])
                shelf_to_product[int(f[0])-1]['product_width_mm'] += p[3]
                shelf_to_product[int(f[0])-1]['profit'] += p[2]
                break
            elif f[2]<p[1]:
                continue
    for i in range(len(shelf_to_product)):
        shelf_to_product[i]['n_products'] = len(shelf_to_product[i]['product_id'])
    x = pd.DataFrame(shelf_to_product)
    return x


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
        "--out", "-o", default="solution_greedy.csv", help="solution output file"
    )

    args = parser.parse_args()

    fixture = pd.read_csv(args.fixture)
    products = pd.read_csv(args.products)

    #alterations to the dataframe arguments
    products = pd.read_csv('products.csv')
    products['profit/mm'] = products['profit']/products['product_width_mm']
    products = products.sort_values('profit/mm', ascending=False)
    fixture = pd.read_csv('fixture.csv')
    fixture['shelf_width_mm'] = fixture['shelf_width_cm'] * 10
    fixture['profit'] = 0

    solution = planogram_greedy(fixture, products)
    
    solution.to_csv(args.out, index=False)
    print('open csv file to see entire solution')
    print("stats:", solution)
