#Your Code Here
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.colors import LinearSegmentedColormap
import ipywidgets as widgets
from IPython.display import display

mean_values = df.mean(axis=1)
std_errors = df.sem(axis=1)
initial_input_value = 42000
colours = [(0,'blue'),(0.5,'white'),(1,'red')]
custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colours)

input_value_slider = widgets.FloatSlider(
    value=initial_input_value,
    min=min(mean_values),
    max=max(mean_values),
    step=0.1,
    description='User Value',
    continuous_update=False
)

def prob(value, mu, se):
    z = (value - mu) / se
    p = norm.cdf(z)
    return p

def update_plot(input_value):
    plt.figure(figsize=(10,6))
    probs = [prob(input_value, mean, std_error) for mean, std_error in zip(mean_values, std_errors)]
    plt.bar(df.index.astype(str), mean_values, yerr=1.96 * std_errors, capsize=20, color=custom_cmap(probs), edgecolor='black', alpha=0.75)
    plt.axhline(y=input_value, color='black', linestyle='--', label=f'Input Value: {input_value}')
    plt.title(f'Bar Graph of Mean Values and 95% error bars')
    plt.xlabel('Years')
    plt.ylabel('Mean Values')
    plt.draw()

display(widgets.interactive(update_plot, input_value=input_value_slider))

plt.show()
