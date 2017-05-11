from sys import stderr
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib.pyplot import figure

def fancyplot(data):
    try:
        from mpl_toolkits.basemap import Basemap
    except ImportError as e:
        print('could not make fancy plot.',e, file=stderr)
        return

    dates = data.items.values
    satnum = data.major_axis
    if dates.size>6:
        print('skipping fancy map plot due to too many times (plot will get overly crowded)', file=stderr)
        return
    #lon and lat cannot be pandas Series, must be values
    for d in data:
        lat= data[d]['lat'].values; lon= data[d]['lon'].values
        ax= figure().gca()
        m = Basemap(projection='merc',
                      llcrnrlat=-80, urcrnrlat=80,
                      llcrnrlon=-180,urcrnrlon=180,
                      lat_ts=20,
                      resolution='c')

        m.drawcoastlines()
        m.drawcountries()
        m.drawmeridians(np.arange(0,360,30))
        m.drawparallels(np.arange(-90,90,30))
        x,y = m(lon,lat)
        m.plot(x,y,'o',color='#dadaff',markersize=14)
        ax.set_title('{} to {}'.format(dates[0],dates[-1]))

        for s,xp,yp in zip(satnum,x,y):
            ax.text(xp,yp,s,ha='center',va='center',fontsize=11)

def doplot(data,obs):
    polar = True

    dates = data.items
    satnum= data.major_axis

    fg = figure()
    ax = fg.gca()
    ax.set_ylabel('lat [deg.]')
    ax.set_xlabel('lon [deg.]')
    ax.set_xlim(-180,180)
    ax.set_ylim(-90,90)
    ax.set_title('{} to {}'.format(dates[0].strftime('%xT%X'), dates[-1].strftime('%xT%X')))
    #ax.grid(True)
    ax.yaxis.set_major_locator(MultipleLocator(15))
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.xaxis.set_major_locator(MultipleLocator(30))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
# %%
    if polar:
        azoffs = 0
        ax2=figure().gca(polar=True)
        ax2.set_theta_zero_location('N')
        ax2.set_theta_direction(-1)
        ''' http://stackoverflow.com/questions/18721762/matplotlib-polar-plot-is-not-plotting-where-it-should '''
        ax2.set_yticks(range(0, 90+10, 10))                   # Define the yticks
        yLabel = ['90', '', '', '60', '', '', '30', '', '', '']
        ax2.set_yticklabels(yLabel)
    else:
        azoffs=3
        ax2 = figure().gca()
        ax2.set_xlabel('azimuth [deg.]')
        ax2.set_ylabel('elevation [deg.]')
        ax2.set_xlim(0,360)
        ax2.set_ylim(0,90)
        ax2.set_title('Azimuth & Elevation by PRN @ ({},{}) from\n{} to {}'.format(obs.lat,obs.lon,dates[0],dates[-1]))
        #ax2.grid(True)
    ax2.set_title('{} to {}'.format(dates[0],dates[-1]))
# %%
    for s in satnum:
        az = data.loc[:,s,'az'].values.astype(float)
        el = data.loc[:,s,'el'].values.astype(float)
        lat= data.loc[:,s,'lat'].values
        lon= data.loc[:,s,'lon'].values #need .values for indexing

        if polar:
            ax2.plot(np.radians(az),
                     90 - el,  # el in degrees
                     marker='.',linestyle='-')
        else:
            ax2.plot(az, el,
                     marker='.',linestyle='-')


        ax.plot(lon,lat, marker='.', linestyle='-')

        if len(dates)<6: #don't want overcrowded plot
            for i,d in enumerate(dates):
                pl = '{} {}'.format(s, d.strftime('%H:%M'))
                ax.text(lon[i]+3, lat[i]+3,pl,fontsize='x-small')
                if np.isfinite(az[i]):
                    ax2.text(np.radians(az[i]+azoffs), 90-el[i],
                             pl, fontsize='x-small')
        else: #just label first point
            #too much text for all satellites and all times (maybe label once per line)
            ax.text(lon[0]+3, lat[0]+3,s,fontsize='small')
            if np.isfinite(az[0]):
                ax2.text(az[0]+azoffs, el[0],
                     s,fontsize='small')