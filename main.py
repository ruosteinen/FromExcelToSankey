import plotly.graph_objects as go
import pandas as pd
import numpy as np

xls = pd.ExcelFile("Sankey ARR.xlsx")

df = pd.read_excel("Sankey ARR.xlsx", sheet_name="Labels", skiprows=[])

#converting columns from Excel to arrays
label = df.iloc[:, 0].to_numpy()
target = df.iloc[:, 1].to_numpy()

combined_data = np.concatenate((label, target))

value = df.iloc[:, 2].to_numpy()
filtered_array = value[~np.isnan(value)]


#dictionary of unique strings
unique_dict = {}

label_names = []

item_number = 0

for item in combined_data:
    if not pd.isna(item) and item not in unique_dict:
        unique_dict[item] = item_number
        label_names.append(item)
        item_number += 1


#print(label_names)

#Replacing elements in label and target with numbers from the dictionary
label_numbers = [unique_dict[item] for item in label if not pd.isna(item)]
target_numbers = [unique_dict[item] for item in target if not pd.isna(item)]

'''
for item, number in unique_dict.items():
    print(f"{item}: №{number}")

print(f"\nКоличество уникальных элементов в объединенных столбцах (исключая null): {len(unique_dict)}")

print("\nПреобразованные данные из label:")
print(label_numbers)

print("\nПреобразованные данные target:")
print(target_numbers)


for item in value:
    if not pd.isna(item):
        print(item)
'''


fig = go.Figure(go.Sankey(

    #"snap" means that , nodes are automatically adjusted
    #to reduce the intersection of links
    #and improve the readability of the diagram

    arrangement = "snap",

    node = {
        "label": label_names,
        "pad": 15,
        "thickness": 20,
        "line": {"color": "black", "width": 0.5}
    },

    link = {
        "source": label_numbers,
        "target": target_numbers,
        "value": filtered_array
    }
))

fig.update_layout(title_text="Sankey for Andrei", font_size=10)
fig.show()
