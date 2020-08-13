import io
import random
from flask import Flask, Response, request
from matplotlib.backends.backend_svg import FigureCanvasSVG

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


app = Flask(__name__)


@app.route("/")
def index():
    """ Returns html with the img tag for your plot.
    """
    num_x_points = int(request.args.get("num_x_points", 50))
    type_x_points = int(request.args.get("type_x_points", 1))
    distribution_x_points = int(request.args.get("distribution_x_points", 1))
    mean = int(request.args.get("mean", 0))
    stdev = int(request.args.get("stdev", 2))
    min = int(request.args.get("min", 0))
    max = int(request.args.get("max", 1))
    lem = int(request.args.get("lem", 1))
    bins = int(request.args.get("bins", 10))
    # in a real app you probably want to use a flask template.
    return f"""


    <h1>Histogram Creation</h1>
    <form method=get action="/">
      <table>
            <tr>
                <td>Sample Size :</td>
                <td><input name="num_x_points" type=number value="{num_x_points}" /></td>
            </tr>
            <tr>
                <td>      Sample Type :</td>
                <td>
                    <input type="radio" name="type_x_points" type=number value="1" />With Replacement</input>
                    <input type="radio" name="type_x_points" type=number value="2" />Without Replacement</input>
                </td>
            </tr>

            <tr>
                <td>Select Distribution :</td>
                <td>
                    <select name="distribution_x_points">
                        <option type=number value="1" />Normal</option>
                        <option type=number value="2" />Uniform</option>
                        <option type=number value="3" />Exponential</option>
                    </select>
                </td>
            </tr>

            <tr>
                <td>Mean :</td>
                <td><input type=number name='mean' value={mean}></td>
                <td>     Stantdard Deviation :</td>
                <td><input type=number name='stdev' value={stdev}></td>
            </tr>
           
            <tr>
                <td>Uniform Minimum :</td>
                <td><input type=number name='min' value={min}></td>
                <td>     Uniform Maximum</td>
                <td><input type=number name='max' value={max}></td>
            </tr>
            <tr>
                <td>Exponential Lembda :</td>
                <td><input type=number name='lem' value={lem}></td>
            </tr>
            <br>
            <tr>
                <td>Enter Number of Bins :</td>
                <td><input type=number name='bins' value={bins}></td>
            </tr>
            <tr><td><input type="submit" value="Get Graph"></td></tr>
        </table>
    </form>

    <h3>Generated Histogram</h3>
    <img src="/matplot-as-image-{num_x_points},{type_x_points},{distribution_x_points},{mean},{stdev},{min},{max},{lem},{bins}.svg"
         alt="random points as svg"
         height="450"
    >

    """
    # from flask import render_template
    # return render_template("yourtemplate.html", num_x_points=num_x_points)


@app.route("/matplot-as-image-<int:num_x_points>,<int:type_x_points>,<int:distribution_x_points>,<int:mean>,<int:stdev>,<int:min>,<int:max>,<int:lem>,<int:bins>.svg")
def plot_svg(num_x_points=50,type_x_points=1,distribution_x_points=1,mean=0,stdev=2,min=0,max=1,lem=1,bins=10):
    """ renders the plot on the fly.
    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    lst=[]
    
    if(distribution_x_points==1):
        if(type_x_points==1):
            lst.append(np.random.normal(mean, stdev, num_x_points))
            axis.hist(lst, bins=bins )
            
        else:
            lst.append(np.random.normal(mean, stdev, num_x_points))
            lst_without_repetition=[]
            for i in lst:
                if i not in lst_without_repetition:
                   lst_without_repetition.append(i)
                else:
                   temp=np.random.normal(mean, stdev,1)
                   lst_without_repetition.append(temp)
                axis.hist(lst_without_repetition, bins=bins)


    elif(distribution_x_points==2):
        if(type_x_points==1): 
            lst.append(np.random.uniform(min, max, num_x_points))
            axis.hist(lst, bins=bins)
        else:
            lst.append(np.random.uniform(min, max, num_x_points))
            lst_without_repetition=[]
            for i in lst:
                if i not in lst_without_repetition:
                   lst_without_repetition.append(i)
                else:
                   temp=np.random.uniform(min,max,1)
                   lst_without_repetition.append(temp)
                axis.hist(lst_without_repetition, bins=bins)


    elif(distribution_x_points==3):
        if(type_x_points==1):
            lst.append(np.random.exponential((1/lem), num_x_points))
            axis.hist(lst, bins=bins)
        else:
            lst.append(np.random.exponential((1/lem), num_x_points))
            lst_without_repetition=[]
            for i in lst:
                if i not in lst_without_repetition:
                   lst_without_repetition.append(i)
                else:
                   temp=np.random.exponential((1/lem), 1)
                   lst_without_repetition.append(temp)
                axis.hist(lst_without_repetition)

    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


if __name__ == "__main__":
    import webbrowser

    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
