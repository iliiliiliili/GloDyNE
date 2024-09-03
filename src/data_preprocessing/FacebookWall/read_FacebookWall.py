"""
http://konect.cc/
or
http://konect.uni-koblenz.de

gap = 1
"""

import networkx as nx
import datetime 
import pickle
import pandas as pd

gap = 1

def save_nx_graph(nx_graph, path='dyn_graphs_dataset.pkl'):
    with open(path, 'wb') as f:
        pickle.dump(nx_graph, f, protocol=pickle.HIGHEST_PROTOCOL)  # the higher protocol, the smaller file

if __name__ == '__main__':
    # --- load data ---
    df = pd.read_csv('FacebookWall.txt', sep=' \t| ', names=['from','to','weight?','time'], header=None, comment='%')
    df['time'] = df['time'].apply(lambda x: int(datetime.datetime.utcfromtimestamp(x).strftime('%Y%m%d')))
    all_days = len(pd.unique(df['time']))
    print('# of all edges: ', len(df))
    print('all unique days: ', all_days)
    print(df.head(5))

    # --- check the time oder, if not ascending, resort it ---
    tmp = df['time'][0]
    for i in range(len(df['time'])):
        if df['time'][i] > tmp:
            tmp = df['time'][i]
        elif df['time'][i] == tmp:
            pass
        else:
            print('not ascending --> we resorted it')
            print(df[i-2:i+2])
            df.sort_values(by='time', ascending=True, inplace=True)
            df.reset_index(inplace=True)
            print(df[i-2:i+2])
            break
        if i == len(df['time'])-1:
            print('ALL checked --> ascending!!!')
    
    # --- generate graph and dyn_graphs ---
    cnt_graphs = 0
    graphs = []
    g = nx.Graph()
    tmp = df['time'][0]   # time is in ascending order
    for i in range(len(df['time'])):    # for each ith line
        if tmp == df['time'][i]:        # if is in current day at ith line
            g.add_edge(str(df['from'][i]), str(df['to'][i]))   # the end
            if i == len(df['time'])-1:  # EOF ---
                cnt_graphs += 1
                # graphs.append(g.copy())  # ignore the last day, which often has some problem...
                print('processed graphs ', cnt_graphs, '/', all_days, 'ALL done......\n')
        elif tmp < df['time'][i]:       # if goes to next day
            cnt_graphs += 1
            if (cnt_graphs//gap) >= (all_days//gap-30) and cnt_graphs%gap == 0: # the last 50 graphs 'and' the gap
                g.remove_edges_from(g.selfloop_edges())
                g.remove_nodes_from(list(nx.isolates(g)))
                print('the latest real world date of the snapshot to be appended ', tmp)  # if gap=1, then tmp here = df['time'][i-1]
                graphs.append(g.copy())     # append previous g; to reduce ROM, only append 30 days
                # g = nx.Graph()            # reset graph, based on the real-world application 
            if cnt_graphs % 50 == 0:
                print('processed graphs ', cnt_graphs, '/', all_days)

            g.add_edge(str(df['from'][i]), str(df['to'][i]))
            tmp = df['time'][i]
        else:
            print('ERROR -- EXIT -- please double check if time is in ascending order!')
            exit(0)
    
    # --- take out and save part of graphs ----
    print('total graphs: ', len(graphs))
    graphs = graphs[-21:]
    save_nx_graph(nx_graph=graphs, path='FacebookWall.pkl')
    for i in range(len(graphs)):
        print('@ graph', i, '# of nodes', len(graphs[i].nodes()), '# of edges', len(graphs[i].edges()))
    print('gap', gap)
    print('the first day: ', df['time'][0])
    print('the last day: ', df['time'][len(df['time'])-1])
    print(pd.unique(df['time']))
    print('the date of the last day for graphs[-21:] here is, ', pd.unique(df['time'])[-2])  # due to ignore the last day
    print('due to ignore the last day')