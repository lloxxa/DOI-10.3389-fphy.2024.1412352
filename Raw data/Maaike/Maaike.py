import glob
from natsort import os_sorted
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import scipy.stats as st
import scipy.signal as sig
from scipy.interpolate import splrep,splev
from scipy.fft import rfft,rfftfreq

#support functions
def getPaths(inputdir): #returns pathlist
    print('Getting paths...')
    if '.csv' in inputdir:
        paths = [inputdir]
    else:
        paths = glob.glob(f'{inputdir}\*.csv') #files in inputdirectory
    if paths == []:
        paths = glob.glob(f'{inputdir}\*\*.csv') #files in subdirectory of inputdirectory (I kno, is shtoepid, maar glob kan dat zelf niet)
    if paths == []:
        paths = glob.glob(f'{inputdir}\*\*\*.csv') #files in subdirectory of subdirectory of inputdirectory
    if len(paths)>1:
        pathlist = os_sorted(paths) # anders doet ie 1,10,11,...,19,2,20,21.... Nu gwn 1,2,3,...,9,10,11,12,...
    else:
        pathlist = paths
    if pathlist == []:
        raise ValueError("No paths are found, trololol!")
    else:
        print('Done!')
    return pathlist
def calcData(inputdir): #returns dictionary {path:dictionary w/ values}
    pathlist = getPaths(inputdir)
    print('Calculating data...')
    alldicts = {}
    if len(pathlist)==1:
        inputdir = inputdir.split('\\')[:-1]
    for path in pathlist:
        # defining baseline and setting up
        interval = int(path.split('_')[-1][:-4])
        file = path.split('\\')[-1]
        if interval==1:
            if 'dict' in locals():
                pathindex = pathlist.index(path)
                alldicts[pathlist[pathindex-1]] = dict
                dict = {'W':[[],[],[]],'F':[[],[],[]],'E':[[],[],[]]}
            else:
                dict = {'W':[[],[],[]],'F':[[],[],[]],'E':[[],[],[]]}
            measurement_temp = file.split('_Interval')[0]
            print(f'Beep boop, working on {measurement_temp}')
        measurement = file.split('_Interval')[0]
        preload = measurement.split('_')[2]
        FN = float(preload.replace('FN','').replace('Fn',''))
        data = pd.read_csv(path, names=['N','F', 'd', 't'],skiprows=1)
        if (interval)%4==1:
            FNbaseline = np.mean(data['F'][:20])
        data['F'] -= FNbaseline

        # baselining and calculating the data
        if interval%4==3 or interval%4==0:
            neg_start = (data['F'].lt(0).idxmax()) #finds first negative value; the new baseline
            if interval%4==3:
                gapbaseline = data['d'][neg_start]
            data['d'] -= gapbaseline
            work = abs(np.trapz(data['F'],data['d'])) #y,x
            if interval%4==3:
                Fc = abs(np.min(data['F']))
                preloadindex = (data['F'].lt(FN).idxmax())
                slope, _ = np.polyfit(data['d'][preloadindex:preloadindex+20],data['F'][preloadindex:preloadindex+20],1)
                Em = slope
            if interval%4==0 and abs(np.min(data['F']))>Fc:
                Fc = abs(np.min(data['F']))

        # appending data to appropriate dictionaries
        if "onespeed" in measurement:
            if interval%4 == 3:#append is faster than +=
                dict["W"][0].append(work)
                dict["F"][0].append(Fc)
                dict["E"][0].append(Em)
            elif interval%4==0:
                # dict["W"][0][-1] += work #k bereken nog geen W voor interval 4n, dus moet nu niet die van int3 2x doen
                dict["F"][0][-1] = Fc
        else:
            if interval%12 == 3:
                dict["W"][0].append(work) #0=500um, 1=100um, 2=10um
                dict["F"][0].append(Fc)
                dict["E"][0].append(Em)
            elif interval%12 == 7:
                dict["W"][1].append(work)
                dict["F"][1].append(Fc)
                dict["E"][1].append(Em)
            elif interval%12==11:
                dict["W"][2].append(work)
                dict["F"][2].append(Fc)
                dict["E"][2].append(Em)
            elif interval%12==4:
                dict["W"][0][-1] += work
                dict["F"][0][-1] = Fc
            elif interval%12==8:
                dict["W"][1][-1] += work
                dict["F"][1][-1] = Fc
            elif interval%12==0:
                dict["W"][2][-1] += work
                dict["F"][2][-1] = Fc
    alldicts[path] = dict
    print('Done!')
    return alldicts

#callable functions
def histogram(dataseries,inputdir):
    alldicts = calcData(inputdir)
    print('Preparing figure...')
    nBins = 10
    if dataseries=='W':
        xlabel='Adhesive work (N.mm)'
        titlepart = "adhesive work"
        roundingDgt = 1
    elif dataseries=='F':
        xlabel='Pull-off force (N)'
        titlepart = "pull-off force"
        roundingDgt = 2
    elif dataseries=='E':
        xlabel='Elastic modulus' #unit??
        titlepart = "elastic modulus"
        roundingDgt = 2
    
    for dict in alldicts:
        measurement = dict.split("\\")[-1].split('_Interval')[0]
        print(f'Now going to show: {measurement}')
        df = alldicts[dict]
        if df['W'][1]==[]: #onespeed
            retrSpeed = ['500um']
        else:
            retrSpeed = ['500um','100um','1um']
        for i in range(len(retrSpeed)):
            fig, ax1 = plt.subplots()
            ax1.hist(df[dataseries][i],bins=nBins)
            ax1.set_xlabel(xlabel)
            ax1.set_ylabel("# occurences")
            mu, sigma = st.norm.fit(df[dataseries][i])
            x = np.linspace(np.min(df[dataseries][i]), np.max(df[dataseries][i]), 30)
            normalFit = st.norm.pdf(x, loc=mu, scale=sigma)
            ax2 = ax1.twinx()
            ax2.plot(x, 100*normalFit,'k--')
            ax2.axes.yaxis.set_visible(False)
            plt.title(f"Histogram of {titlepart}. $\mu$ = {round(mu,roundingDgt)} $\sigma$ = {round(sigma,roundingDgt)}")
            # plt.savefig(f"{measurement}_{dataseries}_hist_{retrSpeed[i]}.pdf")
            plt.show()
            print(f'{measurement}: mean = {round(mu,roundingDgt)} st.dev = {round(sigma,roundingDgt)}')
def timeseries(dataseries,inputdir):
    alldicts = calcData(inputdir)
    print('Preparing figure...')
    if dataseries=='W':
        ylabel='Adhesive work (N/mm?)'
        titlepart = "Adhesive work"
    elif dataseries=='F':
        ylabel='Pull-off force (N)'
        titlepart = "Pull-off force"
    elif dataseries=='E':
        ylabel='Elastic modulus (??)'
        titlepart = "Elastic modulus"
    
    for dict in alldicts:
        measurement = dict.split("\\")[-1].split('_Interval')[0]
        print(f'Now going to showing {measurement}')
        df = alldicts[dict]
        if df['W'][1]==[]: #onespeed
            retrSpeed = ['500um']
        else:
            retrSpeed = ['500um','100um','10um']
        for i in range(len(retrSpeed)):
            plt.plot(df[dataseries][i])
            plt.title(f"{titlepart} over time")
            plt.xlabel("measurement #")
            plt.ylabel(ylabel)
            # plt.savefig(f"{measurement}_{dataseries}_time_{retrSpeed[i]}.pdf")
            plt.show()
def seriesfig(variable,inputdir): #per feature OR total. Comment necessary portion of code.
    alldicts = calcData(inputdir)
    print('Preparing figure...')
    P2_5 = {'variable': [],'avgW':[],'avgF':[],'stdW':[],'stdF':[]}
    P3   = {'variable': [],'avgW':[],'avgF':[],'stdW':[],'stdF':[]}
    P4   = {'variable': [],'avgW':[],'avgF':[],'stdW':[],'stdF':[]}
    for dict in alldicts:
        measurement = dict.split("\\")[-1].split('_Interval')[0]
        divisitor = 1

        # per feature. Comment if you want total.
        if 'P2.5' in measurement or 'P2_5' in measurement:
            divisitor = 110 #11x10
        elif 'P3' in measurement:
            divisitor = 80 # 10x8
        elif 'P4' in measurement:
            divisitor = 42 # 6x7
        # end of per feature

        if variable == 'FN':
            preload = measurement.split('_')[2]
            value = float(preload.replace('FN','').replace('Fn',''))
            xlabel = 'Applied preload (N)'
        elif variable == 'retrSpd':
            retraction_speed = measurement.split('retrSpd')[1][:-9]
            value = float(retraction_speed)
            xlabel = 'Retraction speed ($\mu$m/s)'
        elif variable == 'time':
            day = measurement.split('_day')[1].split('_')[0]
            value = float(day)
            xlabel = 'Time in days'
        print(f'Boop beep, working on {measurement}')
        df = alldicts[dict]
        avgW = np.mean(df['W'][0])/divisitor
        stdW = np.std(df['W'][0])/divisitor
        avgF = np.mean(df['F'][0])/divisitor
        stdF = np.std(df['F'][0])/divisitor
        if 'P2.5' in measurement or 'P2_5' in measurement:
            series = P2_5
        elif 'P3' in measurement:
            series = P3
        elif 'P4' in measurement:
            series = P4
        series['variable'].append(value)
        series['avgW'].append(avgW)
        series['avgF'].append(avgF)
        series['stdW'].append(stdW)
        series['stdF'].append(stdF)
    P2_5 = pd.DataFrame(P2_5)
    P3 = pd.DataFrame(P3)
    P4 = pd.DataFrame(P4)

    #plotting pull-off force over variable
    if len(P2_5['variable'])!=0:
        plt.plot(P2_5['variable'],P2_5['avgF'],label='P2.5',c='C0')
        plt.fill_between(P2_5['variable'],P2_5['avgF']-P2_5['stdF'],P2_5['avgF']+P2_5['stdF'],alpha=0.5,color='C0')
    if len(P3['variable'])!=0:
        plt.plot(P3['variable'],P3['avgF'],label='P3',c='C1')
        plt.fill_between(P3['variable'],P3['avgF']-P3['stdF'],P3['avgF']+P3['stdF'],alpha=0.5,color='C1')
    if len(P4['variable'])!=0:
        plt.plot(P4['variable'],P4['avgF'],label='P4',c='C2')
        plt.fill_between(P4['variable'],P4['avgF']-P4['stdF'],P4['avgF']+P4['stdF'],alpha=0.5,color='C2')
    plt.xlabel(xlabel)
    plt.ylabel('Pull-off force (N)')
    plt.legend()
    plt.show()
    plt.close()

    #plotting work of adhesion over variable # ik heb besloten work of adhesion buiten mijn thesis te houden, maar je kan dit un-commenten om t weer te krijgen
    if len(P2_5['variable'])!=0:
        plt.plot(P2_5['variable'],P2_5['avgW'],label='P2.5',c='C0')
        plt.fill_between(P2_5['variable'],P2_5['avgW']-P2_5['stdW'],P2_5['avgW']+P2_5['stdW'],alpha=0.5,color='C0')
    if len(P3['variable'])!=0:
        plt.plot(P3['variable'],P3['avgW'],label='P3',c='C1')
        plt.fill_between(P3['variable'],P3['avgW']-P3['stdW'],P3['avgW']+P3['stdW'],alpha=0.5,color='C1')
    if len(P4['variable'])!=0:
        plt.plot(P4['variable'],P4['avgW'],label='P4',c='C2')
        plt.fill_between(P4['variable'],P4['avgW']-P4['stdW'],P4['avgW']+P4['stdW'],alpha=0.5,color='C2')
    plt.xlabel(xlabel)
    plt.ylabel('Work of adhesion (N.mm)')
    # plt.legend()
    plt.show()
    plt.close()
def rawfig(inputdir): # shows only retraction
    pathlist = getPaths(inputdir)
    print('Preparing figure...')
    labels = []
    lines = []
    for i,path in enumerate(pathlist):
        # defining baseline and setting up
        interval = int(path.split('_')[-1][:-4])
        file = path.split('\\')[-1]
        measurement = file.split('_Interval')[0]
        data = pd.read_csv(path, names=['N','F', 'd', 't'],skiprows=1)
        if interval == 1:
            colour = f'C{i}'
            line = mlines.Line2D([], [], c=colour)#clrs[i])
            lines.append(line)
            labels.append(measurement)
        if (interval)%4==1:
            FNbaseline = np.mean(data['F'][:20])
        data['F'] -= FNbaseline

        # baselining and calculating the data
        if interval%4==3 or interval%4==0:
            neg_start = (data['F'].lt(0).idxmax()) #finds first negative value; the new baseline
            if interval%4==3:
                gapbaseline = data['d'][neg_start]
            data['d'] -= gapbaseline

        # plotting the data
        if "onespeed" in measurement:
            if interval%4 == 3:# or interval%4==0:
                plt.plot(data['d'],data['F'],label=f'{measurement}',c=colour)
        else:
            if interval%12 == 3 or interval%12==4:
                plt.plot(data['d'],data['F'],label=f'{measurement}',color='r')
            elif interval%12 == 7 or interval%12==8:
                plt.plot(data['d'],data['F'],label=f'{measurement}',color='b')
            elif interval%12==11 or interval%12==0:
                plt.plot(data['d'],data['F'],label=f'{measurement}',color='g') #low speed; not always baselined on interval 3

    if len(pathlist)<5:
        plt.title(f'Force-distance curve of {measurement}')
    else:
        plt.title('Force-distance curves')
    plt.xlabel('Gap (mm)')
    plt.ylabel('Normal force (N)')
    plt.set_cmap('viridis')
    # labels = ['FN5','FN5.2','FN6','FN8']
    plt.legend(handles=lines,labels=labels)
    # plt.savefig(f'{measurement}.pdf')
    plt.show()
    plt.close()
def rawfig_better(inputdir): #shows entire force-distance curve (heeft vgm wel kuren soms tho)
    pathlist = getPaths(inputdir)
    print('Preparing figure...')
    for i,path in enumerate(pathlist):
        # setting up
        interval = int(path.split('_')[-1][:-4])
        file = path.split('\\')[-1]
        labels = []
        if 'measurement' in locals():
            prev_measurement = measurement
        measurement = file.split('_Interval')[0]
        data = pd.read_csv(path, names=['N','F', 'd', 't'],skiprows=1)
        if interval==1:
            labels.append(measurement)
            print(f'Working on {measurement}...')
            colour = f'C{i}'
        #merging data
        if interval%4==1 and 'temp' in locals():
            temp['d'] -= gapbaseline #maar dan voor alle d's in temp
            plt.plot(temp['d'],temp['F'],label=f'{prev_measurement}',c=colour)
        #baselining data
        if interval%4==1:    
            FNbaseline = np.mean(data['F'][:20])
            data['F'] -= FNbaseline
            temp = data
        else:
            data['F'] -= FNbaseline
            temp = temp.append(data,ignore_index=True)
        if interval%4==3:
            neg_start = (data['F'].lt(0).idxmax()) #finds first negative value; the new baseline
            gapbaseline = data['d'][neg_start]
        if interval%4==0:
            neg_start_4 = (data['F'].lt(0).idxmax())
            if data['d'][neg_start_4] > data['d'][neg_start]:
                neg_start = neg_start_4
    
    temp['d'] -= gapbaseline #maar dan voor alle d's in temp
    plt.plot(temp['d'],temp['F'],c='C0')
    # establishing plot layout
    plt.xlabel('Gap (mm)')
    plt.ylabel('Normal force (N)')
    # plt.savefig(f'{measurement}.pdf')
    # labels = ['FN5','FN5.2','FN6','FN8']
    plt.legend(labels=labels)
    plt.show()
    plt.close()
def spreadfig(inputdir): # deze is kinda broken bij extreme waarden omdat t niet goed wil alignen... I tried...
    pathlist = getPaths(inputdir)
    print('Preparing figure...')
    labels = []
    lines = []
    for i,path in enumerate(pathlist):
        # setting up
        interval = int(path.split('_')[-1][:-4])
        file = path.split('\\')[-1]
        if 'measurement' in locals():
            measurement_prev = measurement
        measurement = file.split('_Interval')[0]
        data = pd.read_csv(path, names=['N','F', 'd', 't'],skiprows=1)
        if interval==1:
            colour = f'C{i}'
            line = mlines.Line2D([], [], c=colour)
            lines.append(line)
            labels.append(measurement)

        #merging data
        if interval%4==1 and 'temp' in locals():
            temp['d'] -= gapbaseline
            if 'df_F' in locals():
                df_F[f'F int.{interval-4}'] = pd.DataFrame(temp['F'])
                df_d[f'd int.{interval-4}'] = pd.DataFrame(temp['d'])
                if interval==1 and 'df_F' in locals():
                    print(f'Working on {measurement_prev}...')
                    # aligning the F # hij doet wat ie moet doen, maar dat lijkt niet zo te helpen tho lol
                    # alignment_index = {}
                    # index_shift = {}
                    # for columnname, column in df_F.items():
                    #     alignment_index[columnname] = column.gt(0.05).idxmax()
                    #     index_shift[columnname] = alignment_index[columnname]-alignment_index['F']
                    # for columnname, column in df_F.items():
                    #     # if columnname != 'F':
                    #     #     df_F[columnname] = df_F[columnname].shift(index_shift[columnname])
                    #     if columnname == 'F':
                    #         df_F_shift = df_F[columnname]
                    #     else:
                    #         df_F[columnname].index = df_F[columnname].index+index_shift[columnname]
                    #         df_F_shift = pd.concat([df_F_shift, df_F[columnname]], axis=1)
                    #     df_F = df_F_shift

                    # calculating means and spreads, plotting them (F over index cuz 0-point of d is at basically the same index each time)
                    std_F = df_F.std(axis='columns')
                    avg_F = df_F.mean(axis='columns')
                    avg_d = df_d.mean(axis='columns')
                    std_Fdf = pd.DataFrame(std_F)
                    plt.plot(avg_d,avg_F,c=colour)
                    plt.fill_between(list(avg_d),list(avg_F-std_F),list(avg_F+std_F),alpha=0.5,color=colour)
            else:
                df_F = pd.DataFrame(temp['F'])
                df_d = pd.DataFrame(temp['d'])
        #baselining data
        if interval%4==1:    
            FNbaseline = np.mean(data['F'][:20])
            data['F'] -= FNbaseline
            temp = data
        else:
            data['F'] -= FNbaseline
            temp = temp.append(data,ignore_index=True)
        if interval%4==3:
            neg_start = (data['F'].lt(0).idxmax()) #finds first negative value; the new baseline
            gapbaseline = data['d'][neg_start]
        if interval%4==0:
            neg_start_4 = (data['F'].lt(0).idxmax())
            if data['d'][neg_start_4] > data['d'][neg_start]:
                neg_start = neg_start_4
    # plot last measurement
    print(f'Working on {measurement_prev}...')
    temp['d'] -= gapbaseline
    df_F[f'F int.{interval-4}'] = pd.DataFrame(temp['F'])
    df_d[f'd int.{interval-4}'] = pd.DataFrame(temp['d'])
    std_F = df_F.std(axis='columns')
    avg_F = df_F.mean(axis='columns')
    avg_d = df_d.mean(axis='columns')
    plt.plot(avg_d,avg_F,c='C0')
    plt.fill_between(list(avg_d),list(avg_F-std_F),list(avg_F+std_F),alpha=0.5,color='C0')

    # establishing plot layout
    plt.xlabel('Gap (mm)')
    plt.ylabel('Normal force (N)')
    if len(labels)<7:
        plt.legend(handles=lines,labels=labels)
    # plt.savefig(f'{measurement}.pdf')
    plt.set_facecolor('white')
    plt.show()
    plt.close()
def FT(inputdir): #Lombscargle or FFT, comment and uncomment necessary parts
    pathlist = getPaths(inputdir)
    print('Preparing figure...')
    paths={int(path.split('_Interval_')[-1][:-4]):path for path in pathlist}
    if '_retrSpd' in pathlist[0]:
        retrSpd = int(pathlist[0].split('_retrSpd')[-1].split('_')[0])/1000
    else:
        retrSpd = 0.5
    freq=np.logspace(-0.8,3,num=200)
    p_cutoff = 0.01
    fftsignificance = np.log(len(freq)/p_cutoff)
    for path in paths:
        if path==1:
            slct  = [path,path+1,path+2] #intervals 1,2,3
            retr  = path+2
            datas = {n:pd.read_csv(paths[n]) for n in slct}

            # fitting data to make it evenly spaced and gapless #
            distance_temp  = pd.DataFrame(datas[retr]['Time [s]']*retrSpd)
            distance = distance_temp-distance_temp.iloc[0]
            datas[retr]['Gap [mm]'] = distance
            tck = splrep(datas[retr]['Gap [mm]'], datas[retr]['Normal Force [N]'],s=0.01) #0.001 ideaal voor normale punten, 0.10 ideaal voor 0-lijn
            tmax = round(np.max(datas[retr]['Gap [mm]']),4)
            tmin = round(np.min(datas[retr]['Gap [mm]']),4)
            x = np.arange(tmin,tmax,0.0025) #0.0025 voor time, 0.05 voor gap
            y = splev(x,tck)
            # FFT #
            ft_FFT = {retr:rfft(y)}
            xft_FFT = {retr:rfftfreq(len(y), 0.0025)*2*np.pi}
            # # seperate figures FFT #
            # fig,[ax1,ax2] = plt.subplots(1,2)
            # ax1.plot(datas[retr]['Gap [mm]'],datas[retr]['Normal Force [N]'],'o')
            # ax1.plot(x,y,'.',markersize=5)
            # ax1.legend(['normaal','spline'])
            # ax2.plot(xft_FFT[retr], ft_FFT[retr])
            # ax2.semilogx()

            # Lombscargle section #
            ft_LS = {retr:sig.lombscargle(x,y,freq)}
            # # seperate figures Lombscargle #
            # grad = {retr:np.gradient(datas[retr]['Normal Force [N]'], datas[retr]['Gap [mm]'])}
            # fig,[ax1, ax2]=plt.subplots(2, 1)
            # [ax1.plot(datas[n]['Gap [mm]'], datas[n]['Normal Force [N]'], marker='.') for n in slct] #normale plot
            # ax1.plot(datas[retr]['Gap [mm]'], grad[retr], ls=':', lw=0.8, mfc='None') #afgeleide
            # ax2.axhline(y = fftsignificance, color = 'red', linestyle = '-',lw=0.5,ls=':')
            # ax2.plot(freq, ft_LS[retr], ls='-.', lw=1,marker='.') #fft plot
            # ax2.semilogx()

            # average figures #
            if 'fts_LS' in locals() or 'fts_FFT' in locals():
                fts_LS[retr]  = pd.DataFrame(ft_LS)
                fts_FFT[retr] = pd.DataFrame(ft_FFT)
            else:
                fts_LS  = pd.DataFrame(ft_LS)
                fts_FFT = pd.DataFrame(ft_FFT)
    ft_LS_avg  = fts_LS.mean(axis='columns')
    ft_FFT_avg = fts_FFT.mean(axis='columns')

    fig,[ax1,ax2]=plt.subplots(2,1)
    # ax1 is Lomb-Scargle #
    ax1.axhline(y = fftsignificance, color = 'red', linestyle = '-',lw=0.5,ls=':')
    ax1.plot(freq,ft_LS_avg,ls='-.', lw=1,marker='.')
    ax1.semilogx()
    # ax2 is FFT # # door log-schaal bereik je nooit 0, en de eerste waarde is een 0-waarde, vandaar de horizontale lijn links.
    ax2.plot(xft_FFT[retr],abs(ft_FFT_avg)) #abs because the data is partially imaginary (negative)
    ax2.semilogx()
    # Diagram > normaleplot: wavelength = 1/(freq/2pi) # Lombscargle
    # Normaleplot > diagram: freq = 2pi/wavelength
    fig.supxlabel('Frequency (mm$^{-1}$)')
    fig.supylabel('Intensity')
    plt.show()
    plt.close()

# dir = r'C:\Users\Gebruiker\OneDrive - Wageningen University & Research\Maaike\Convert_output\FN loops'
dir = r'C:\Users\Gebruiker\OneDrive - Wageningen University & Research\Maaike\Convert_output\retrSpd'
# dir = r'C:\Users\Gebruiker\OneDrive - Wageningen University & Research\Maaike\Convert_output\Timeseries\P3'
# dir = r'C:\Users\Gebruiker\OneDrive - Wageningen University & Research\Maaike\Convert_output\FN loops\P3_FNloop_newsample\Eco_P3_FN4_v_onespeed'

# histogram('F',dir) # 'F'/'W'/'E'
# timeseries('F',dir) # 'F'/'W'/'E'
seriesfig('retrSpd',dir) #'time'/'FN'/'retrSpd'
# rawfig(dir) # plots only retraction
# rawfig_better(dir) # plots entire force-distance curve
# spreadfig(dir)
# FT(dir)
