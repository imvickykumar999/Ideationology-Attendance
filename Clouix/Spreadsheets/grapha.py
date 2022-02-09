def plotme(data):
    import pandas as pd
    import numpy as np

    df = pd.DataFrame(data)
    df.index +=1

    dc = {}
    col = list(df.columns)[1:]

    for i in range(len(col)):
        dc.update({col[i] : sum(df[col[i]] == 'P')})

    import matplotlib.pyplot as plt
    import io, base64

    img = io.BytesIO()
    y = list(dc.values())
    # x = list(dc.keys())

    x = []
    for i in range(len(col)):
        a = chr(65+i)
        x.append(a)

    fig = plt.figure(figsize = (5, 5))
    plt.bar(x, y, color ='red', width = 0.4)
    plt.grid(True)
    # plt.xticks(rotation=90)

    plt.ylabel("No. of Attendance  --->")
    plt.title("Attendance Frequency : Bar Graph\n")

    plt.savefig(img, format='png')
    img.seek(0)

    plotted = base64.b64encode(img.getvalue()).decode()
    # print(type(plotted))
    return plotted, dict(zip(x, col))
