import matplotlib.pyplot as plt
import numpy as np

def plotting(df, lang, title = ''):

    # Setting color map for general (viridis) or specific titles (inferno)
    if title == '':
        cmap = plt.cm.viridis
    else:
        cmap = plt.cm.inferno

    ##First plot: Countries
    countries=df[df['Publication Country']!='']
    graph = countries['Publication Country'].value_counts().head(20)
    
    bar_colors = cmap(np.linspace(0, 1, 20))
    
    graph.plot(kind='bar', color = bar_colors)
    plot1title='Cantidad de tesis '+title+' según país de publicación'
    plt.suptitle(plot1title)
    plt.xticks(rotation=45)
    plot1title = str(plot1title)+'.png' 
    plt.tight_layout()
    plt.savefig(plot1title)
    plt.show()

    ##Second plot: Year
    datepublishing = df['Publication year'].value_counts().reset_index().sort_values('Publication year')
    datepublishing.set_index('Publication year')
    print(datepublishing)
    yearmax=datepublishing[datepublishing['count']==datepublishing['count'].max()]['Publication year']
    year=datepublishing[datepublishing['count']==datepublishing['count'].max()]['Publication year']
    countmax = datepublishing['count'].max()

    year=datepublishing['Publication year']
    count=datepublishing['count']
    print('El año con más cantidad de tesis publicadas fue {}'.format(year))
    
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.plot(year,count)
    
    ax.vlines(x=yearmax, ymin=0, ymax=countmax, colors='violet', linestyles='--')
    ax.scatter(yearmax, countmax, color='violet', zorder=5)
    ax.text(yearmax, countmax, f'{countmax}', ha='left', va='bottom', color='violet')

    
    plot2title="Cantidad de tesis "+title+" por año de publicación"
    ax.set_title(plot2title)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plot2title = str(plot2title)+'.png'
    plt.tight_layout()
    plt.savefig(plot2title)
    plt.show()


    
    # Third plot: Languages
    fig, ax = plt.subplots(figsize=(6, 8))
    lang_counts = df['Language'].value_counts().head(20)
    # Create color map for languages
    cmap = plt.cm.tab20   
    bar_colors = cmap(np.linspace(0, 1, len(lang_counts)))

    # Replace labels for languages
    labels = [lang.get(code, code) for code in lang_counts.index]

    bars = ax.bar(labels, lang_counts.values, color=bar_colors)
    # Values for each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,   # posición x en el centro de la barra
            height,                            # posición y arriba de la barra
            f'{height}',                       # texto con el valor
            ha='center', va='bottom', fontsize=9, rotation=0
        )
    ax.set_xticklabels(labels, rotation=45, ha='right')
    plot3title="Distribución de tesis "+title+" por idioma"
    ax.set_title(plot3title)
    ax.set_ylabel("Cantidad de tesis")
    plt.tight_layout()
    plot3title=str(plot3title)+'.png'
    plt.savefig(plot3title)
    plt.show()
