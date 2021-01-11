import pandas as pd
import numpy as np
from pybliometrics.scopus import ScopusSearch

def h_index_year(auth_ID, h_index_year=1960):
    """
    Function to computer H index for the last h_index_year years.

    Keyword arguments:
    auth_ID -- it can be both the ID (usually 11 numbers) or the EID (for ref see SCOPUS)
    h_index_year -- the oldest year, not included. e.g. when searching for each index in the last 15 years --> 2004

    output:
    h_index -- the H index computed on documents published in h_index_year-today
    
    """
    print(auth_ID)
    if len(auth_ID)>11:
        ID=auth_ID[-11:]
    elif len(auth_ID)==11:
        ID=auth_ID
    else:
        raise Exception(
            "Author ID not valid")
    
    api_search="AU-ID({})AND PUBYEAR > {}".format(ID, h_index_year)
    s = ScopusSearch(api_search)
    s.get_results_size()
    tot_eids=s.get_eids()
    cit_list=[]
    #get citations for each document and create a dataframe
    for idx,eid in enumerate(tot_eids):
        s = ScopusSearch("EID({})".format(eid))
        df_tmp=pd.DataFrame(s.results)      
        cit_list.append(int(df_tmp["citedby_count"][0]))
        
    df_cit = pd.DataFrame(cit_list, columns=["citations"]) 
    #compute H index
    for num in range(df_cit.shape[0]):
        work=np.sum(df_cit["citations"]>=num)
        if work>num:
            continue
        elif work==num:
            h_index=num
            break
        elif work<num:
            h_index=num-1
            break
        
    print("final h index",h_index)
    return (int(h_index))
