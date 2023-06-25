#%%
import pandas as pd
import matplotlib.pyplot as plt
#%%
df = pd.read_csv("products_detail_tiki.csv")

df.info()
df.describe()

def get_top_10_seller_quantity_sold_by_category(category_id):
    data = df[df['categories_id'].str.contains(category_id)]
    data = data.groupby(['seller_name'])['quantity_sold'].sum()
    data = data.sort_values(ascending=False)[:10]

    return data
def vendor_item_qty_plot(df, category_id):
    fig = plt.figure(figsize=(8, len(df)/3)) 
    ax = fig.add_subplot(111)
    df.plot.barh(color='#3781ee', ax=ax)

    ax.set_title(get_category_name(category_id) + ' (Top 10 Sellers)', fontsize=16, loc='left', pad=10)
    ax.set_ylabel('Seller Name')
    ax.tick_params(rotation='auto')
    ax.set_xlabel('Quantity Sold', x=0.5, labelpad=10)
    spine_names = ('top', 'right', 'bottom', 'left')
    for spine_name in spine_names:
        ax.spines[spine_name].set_visible(False)

def get_category_name(category_id):
    data = df[df['categories_id'].str.contains(category_id)]
    categories_id = data.iloc[0,:]['categories_id'].split('/')
    categories_name = data.iloc[0,:]['categories_name'].split('/')

    return categories_name[categories_id.index(category_id)]

def get_products_in_category(category_id):
    data = df[df['categories_id'].str.contains(category_id)]
    return data

data = get_products_in_category('2584')
vendor_item_qty_plot(get_top_10_seller_quantity_sold_by_category('2582'), '2582')


# %%
