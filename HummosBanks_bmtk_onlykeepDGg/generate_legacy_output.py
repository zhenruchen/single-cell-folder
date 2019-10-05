import pandas as pd
import numpy as np
import os

def generate_hummos_output(filename,outdir,output_prefix='bmtk_'):
    
    cell_nums = [30,63,8,8,384,32,32]

    df = pd.read_csv(filename, delimiter=' ',header=None)
    df.rename(index=str, columns={0: "time", 1: "cell"},inplace=True)
    df=df.reindex(columns=['cell','time'])
   
    cell_start = np.cumsum(cell_nums)-cell_nums

    for i,start in enumerate(cell_start):
        begin = start
        if i+1 < len(cell_start):
            end = cell_start[i+1]
        else:
            end = 99999999999

        df_sub = df[(df['cell'] >= begin ) & (df['cell'] < end )]

        df_sub['cell'] = df_sub['cell'] - start

        df_sub.sort_values(['time'],inplace=True)

        outname = output_prefix + 'SpikeTime' + str(i) + '.txt'
        outpath = os.path.join(outdir,outname)
        df_sub.to_csv(outpath,header=None,index=False)

if __name__ == '__main__':
    generate_hummos_output('output/spikes.csv','legacy')
    # From MATLAB run Correlation('bmtk_','../HummosBanks-bmtk/legacy/')
    # in the original Hummos directory