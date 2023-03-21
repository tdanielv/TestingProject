import os.path

import requests
import matplotlib.pyplot as plt
import pandas as pd
import json
import seaborn
from sklearn.metrics import confusion_matrix as cm


class DrawingPlots():

    def __init__(self, json_data):
        self.df = pd.read_json(json_data)

    def draw_plots(self):
        def draw(x,y):
            plt.scatter(self.df[x], self.df[y])
            plt.title('График {0} к {1}'.format(x, y))
            plt.xlabel(x)
            plt.ylabel(y)
            path = os.path.join(os.getcwd()+'/plots/',f'{x}_{y}.png')
            plt.savefig(path)
            plt.show()

        draw('mean', 'ceiling_mean')
        draw('max', 'ceiling_max')
        draw('min', 'ceiling_min')

        draw('mean', 'floor_mean')
        draw('max', 'floor_max')
        draw('min', 'floor_min')

        draw('ceiling_mean', 'floor_mean')
        draw('ceiling_max', 'floor_max')
        draw('ceiling_min', 'floor_min')

        # Матрица путаницы
        gt_corners = self.df['gt_corners']
        rb_corners = self.df['rb_corners']
        indexes = self.df['gt_corners'].unique()
        confus_matrix = pd.DataFrame(
            cm(gt_corners, rb_corners), index = [i for i in indexes],columns =[i for i in indexes])
        seaborn.heatmap(confus_matrix, annot=True,  fmt='g')

        plt.xlabel('Real')
        plt.ylabel('Predicted')
        path = os.path.join(os.getcwd() + '/plots/', f'confusion_matrix.png')
        plt.title('Матрица путаницы')
        plt.savefig(path)
        plt.show()

        def pathes_to_plots():
            files = os.listdir('plots/')
            return [os.path.abspath(os.path.join('plots/', file)) for file in files]

        return [i for i in pathes_to_plots()]

def main():
    url = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open('data.json', 'w') as file:
            json.dump(data, file)
    else:
        print('Url is incorrect')
    with open('data.json', 'r') as data:
        a = DrawingPlots(data)
        print(a.draw_plots())

if __name__ == "__main__":
    main()


