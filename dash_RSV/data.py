# import pandas as pd
#
# df = pd.read_excel(r'C:\Users\1\Desktop\Новое приложение ОГК\ogk_web\ogk_web\dash_RSV\prices.xlsx',index_col=0)
# cols=[col.split()[0]+' '+col.split()[1] for col in df.columns]
# st=list(set(cols))
# df_st = pd.DataFrame(index=df.index,columns=st)
# df.columns=cols
# for col in st:
#     try:
#         df_st[col]=df[col].mean(axis=1)
#     except:
#         df_st[col]=df[col].values
#
#
# print(df_st)
