# https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html

from statistics import mean
import pandas._testing as tm
import numpy as np
import pandas as pd
import datetime

df_test = tm.makeTimeDataFrame(nper=3)

# ------------------------------------------------------------------------------
# pivoting
# ------------------------------------------------------------------------------
"stacked"
# N,K = df_test.shape   #(3,4)
# data = {
#     "value":    df_test.to_numpy().ravel("F"),
#     "variable": np.asarray(df_test.columns).repeat(N),
#         "date": np.tile(np.asarray(df_test.index), K),
# }
# pd.DataFrame(data, columns=["date", "variable", "value"])


def unpivot(frame):
    N, K = frame.shape
    data = {
        "value": frame.to_numpy().ravel("F"),
        "variable": np.asarray(frame.columns).repeat(N),
        "date": np.tile(np.asarray(frame.index), K),
    }
    return pd.DataFrame(data, columns=["date", "variable", "value"])


df = unpivot(df_test)
# ------------------------------------------------------------------------------
df_pivoted = df.pivot(index="date", columns="variable", values="value")
            # pd.pivot(df, index="date", columns="variable", values="value")
            # df.pivot_table(index="date", columns="variable", values="value")
df_pivoted.columns
df_test.equals(df_pivoted)  # True
# ------------------------------------------------------------------------------
df['value2'] = df.value*2
df
df_pivoted2 = df.pivot(index="date", columns="variable")
df_pivoted2.columns      # MultiIndex
df_pivoted2.value2
# ------------------------------------------------------------------------------
# stacking and unstacking¶
# ------------------------------------------------------------------------------
pair = list(zip(*[
    ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
    ["one", "two", "one", "two", "one", "two", "one", "two"],
]))
idx = pd.MultiIndex.from_tuples(pair, name=["1st", "2nd"])
arry_test = np.random.randn(8, 2)

df = pd.DataFrame(arry_test, index=idx, columns=['A', 'B'])
df2 = df[:4]

df2_stacked = df2.stack()      # Series
df2.equals(df2_stacked.unstack())  # True

df2_stacked.unstack().equals(df2_stacked.unstack(2))  # 2nd index를 col로
df2_stacked.unstack(1)
# ------------------------------------------------------------------------------
# melting
# https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html#reshaping-by-melt
# ------------------------------------------------------------------------------
cheese = pd.DataFrame(
    {
        "first": ["John", "Mary"],
        "last": ["Doe", "Bo"],
        "height": [5.5, 6.0],
        "weight": [130, 150],
    }
)
cheese.shape  # (2,4)

cheese.melt(id_vars=["first", "last"])   # ids, variable, value
# cheese.melt(id_vars=["first", "last"], var_name="quantity")
# ------------------------------------------------------------------------------
idx = pd.MultiIndex.from_tuples(
    [("person", "A"), ("person", "B")]
)
cheese.index = idx
cheese
cheese.melt(id_vars=["first", "last"])
cheese.melt(id_vars=["first", "last"], ignore_index=False)
# ------------------------------------------------------------------------------

cheese.groupby(level=0).mean()        # cheese.groupby(level=0, axis=0).sum()
cheese.groupby(level=1).mean()

df = pd.DataFrame(
    {
        "A": ["one", "one", "two", "three"] * 6,
        "B": ["A", "B", "C"] * 8,
        "C": ["foo", "foo", "foo", "bar", "bar", "bar"] * 4,
        "D": np.random.randn(24),
        "E": np.random.randn(24),
        "F": [datetime.datetime(2013, i, 1) for i in range(1, 13)]
           + [datetime.datetime(2013, i, 15) for i in range(1, 13)],
    }
)
table = df.pivot_table(index=['A', 'B'], columns=['C'], values=["D","E"], aggfunc=np.mean, margins=True)
table.stack()


pd.crosstab(df['A'], df['B'])

tuples = [('A', 'a'), ('A', 'b'), ('B', 'a'), ('B', 'b')]
index = pd.MultiIndex.from_tuples(tuples)
data = [2, 4, 6, 8]
df = pd.DataFrame(data=data, index=index, columns=['value'])
print(df)
print(df.columns)


reset_df = df.reset_index()
reset_indx1 = df.reset_index(level)
