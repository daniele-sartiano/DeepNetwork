#!/usr/bin/env python

import plotly.plotly as py
import plotly.io as pio

class FlowAnalyzer:
    def __init__(self):
        pass

    def make_chart(self, file_name='chart.png'):
        data = dict(
            type='sankey',
            node = dict(
              pad = 15,
              thickness = 20,
              line = dict(
                color = "black",
                width = 0.5
              ),
              label = ["A1", "A2", "B1", "B2", "C1", "C2"],
              color = ["blue", "blue", "blue", "blue", "blue", "blue"]
            ),
            link = dict(
              source = [0,1,0,2,3,3],
              target = [2,3,3,4,4,5],
              value = [8,4,2,8,4,2]
          ))

        layout =  dict(
            title = "Basic Sankey Diagram",
            font = dict(
              size = 10
            )
        )

        fig = dict(data=[data], layout=layout)
        pio.write_image(fig, file_name)
        

def main():
    fa = FlowAnalyzer()
    fa.make_chart()
    
if __name__ == '__main__':
    main()
