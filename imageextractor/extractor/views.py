from django.shortcuts import render

# Create your views here.



from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
# from skimage.color import rgb2lab, deltaE_cie76
import urllib.request
import json

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def get_colors(image, number_of_colors, show_chart):
    
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    
    counts = Counter(labels)
    
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i]/255 for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]*255) for i in counts.keys()]
    rgb_colors = [ordered_colors[i]*255 for i in counts.keys()]
    
    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = ordered_colors)
    
    return hex_colors





@api_view(['POST'])
def getSingleColor(request):
    jsonData = json.loads(request.body)
    data = urllib.request.urlretrieve(jsonData['imageURI'], 'img.png')
    colorArray = get_colors(get_image('img.png'), 1, False)
    print(colorArray[0])
    # return Response(jsonData['name'])
    return Response(colorArray[0])
    # return Response("Hi")



@api_view(['POST'])
def getNColors(request):
    jsonData = json.loads(request.body)
    data = urllib.request.urlretrieve(jsonData['imageURI'], 'img.png')
    n = jsonData['numberOfColors']
    colorArray = get_colors(get_image('img.png'), n, False)
    print(colorArray)
    # return Response(jsonData['name'])
    return Response(colorArray)
    # return Response("Hi")