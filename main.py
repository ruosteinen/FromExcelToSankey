import plotly.graph_objects as go
import pandas as pd
import numpy as np

xls = pd.ExcelFile("Sankey ARR.xlsx")

df = pd.read_excel("Sankey ARR.xlsx", sheet_name="Labels", skiprows=[])

#converting columns from Excel to arrays
label = df.iloc[:, 0].to_numpy()
target = df.iloc[:, 1].to_numpy()
combined_data = np.concatenate((label, target))

#dictionary of unique strings
unique_dict = {}

item_number = 1

for item in combined_data:
    if not pd.isna(item) and item not in unique_dict:
        unique_dict[item] = item_number
        item_number += 1


#Replacing elements in label and target with numbers from the dictionary
labels_numbers = [unique_dict[item] for item in label if not pd.isna(item)]
target_numbers = [unique_dict[item] for item in target if not pd.isna(item)]

print(labels_numbers)
print(target_numbers)

labels_names = [item for item in label if not pd.isna(item) and item in unique_dict]

# print labels_names for checking
#print(labels_names)

for item, number in unique_dict.items():
    print(f"{item}: №{number}")

'''
print(f"\nКоличество уникальных элементов в объединенных столбцах (исключая null): {len(unique_dict)}")

print("\nПреобразованные данные из label:")
print(labels_numbers)

print("\nПреобразованные данные target:")
print(target_numbers)
'''


value = df.iloc[:, 2].to_numpy()

for item in value:
    if not pd.isna(item):
        print(item)


fig = go.Figure(go.Sankey(

    #"snap" means that , nodes are automatically adjusted
    #to reduce the intersection of links
    #and improve the readability of the diagram

    arrangement = "snap",

    node = {
        "label": labels_names,
        "pad": 15,
        "thickness": 20,
        "line": {"color": "black", "width": 0.5}
    },

    link = {
        "source": labels_numbers,
        "target": target_numbers,
        "value": value
    }
))

fig.update_layout(title_text="Sankey for Andrei", font_size=10)
fig.show()
