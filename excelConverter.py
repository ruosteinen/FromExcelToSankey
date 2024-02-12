import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_sankey_diagram(df):
    label = df.iloc[:, 0].to_numpy()
    target = df.iloc[:, 1].to_numpy()
    combined_data = np.concatenate((label, target))
    value = df.iloc[:, 2].to_numpy()
    percent = df.iloc[:, 3].to_numpy() * 100
    
    unique_dict = {}
    label_names = []
    item_number = 0
    for item in combined_data:
        if not pd.isna(item) and item not in unique_dict:
            unique_dict[item] = item_number
            label_names.append(item)
            item_number += 1

    percent_info_dict = {}
    for i, (lbl, tgt) in enumerate(zip(label, target)):
        if not pd.isna(lbl) and not pd.isna(tgt) and not pd.isna(value[i]):
            if lbl not in percent_info_dict:
                percent_info_dict[lbl] = []

                
            percent_info_dict[lbl].append((tgt, value[i], percent[i]))

    updated_label_names = []
    for name in label_names:
        if name in percent_info_dict:
            
            info_str = "<br>" + "<br>".join([f"{tgt}: ${str(v)} ({str(p)}%)" for tgt, v, p in percent_info_dict[name]])
            updated_label_names.append(f"{name}<br>{info_str}")
        else:
            updated_label_names.append(f"{name}<br>")

    label_numbers = [unique_dict[item] for item in label if not pd.isna(item)]
    target_numbers = [unique_dict[item] for item in target if not pd.isna(item)]

    fig = go.Figure(go.Sankey(
        arrangement="freeform",
        node={
            "label": updated_label_names,
            "pad": 15,
            "thickness": 20,
            "line": {"color": "black", "width": 0.5},
        },
        link={
            "source": label_numbers,
            "target": target_numbers,
            "value": value[~np.isnan(value)]  
        }
    ))

    fig.update_layout(title_text="Sankey Diagram with Values and Percentages", font_size=12)
    fig.show()

    return fig

#Debug

if __name__ == "__main__":
    df = pd.read_excel('excel.xlsx', sheet_name='sankey')
    create_sankey_diagram(df)
