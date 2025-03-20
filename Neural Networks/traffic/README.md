# **CS50AI - project Traffic**

## Task

Write a Python script that, using a neural network, will determine the accuracy of traffic sign recognition using other images of that sign from the available database as knowledge on the basis of which recognition is performed.

## Concept

As AI develops, its application spreads to all areas of life. The development of sensors and digital cameras makes it possible to automate even tasks such as driving a car.

In order for this to be possible, it is necessary to create software capable of determining from the images of the car's camera what kind of environment it is in - in this case, to recognize the traffic signs that the car encounters.

## Approach

The primary goal of this script is to enable the recognition of traffic signs by computer vision using a neural network. Although efficiency is most important, costs must also be taken into account: in this case data processing time, energy consumption and hardware prices.

Data processing time is crucial because the car cannot slow down at every sign to recognize it. More robust hardware can process data faster but is more expensive and consumes more energy that is limited in the car. Also, the hardware has to perform many tasks, not only the recognition of traffic signs. Because of all this, a compromise solution must be made that will give the best relationship between traffic sign recognition and costs.

#### Neural network efficiency

One of the best ways to see the effectiveness of a neural network in relation to its structure is through experimentation with [playground.tensorflow](https://playground.tensorflow.org). If we use the "Circle" initial state, two input cells and a neural network of six hidden layers with two cells in each, we will not be able to solve the problem satisfactorily.

But if we use only one hidden layer with three cells, we will get a good solution in short time. In 10.5 seconds, the training loss is 0.050. We get the same result with one hidden layer and four cells in 7 seconds. With two hidden layers with three cells each, we get the same result in 8 seconds.

The conclusion is that a wider neural network with fewer hidden layers is better for this task. This may not be the case for other situations, but it gives us a good basis for comparison in our project.

## Script

### input images

Input directory is too large, over 26 000 images. Many images are almost identical, which unnecessarily increases already excessive volume of calculations. Even when the number of images is reduced to 6,000, it takes 16 seconds per epoch to compute, which makes this program with that dataset unusable for its intended purpose.

The task is to complete two functions:

### Load_data funkcion

The load_data function should accept and process images of traffic signs. Images should be read and resized with OpenCV-Python module ([cv2 - well explained](https://konfuzio.com/en/cv2/)) as TensorFlow accepts input data mostly as NumPy arrays or tf.data.Dataset objects.

### Get_model funkcion

In this function, a convolutional neural network model is created, consisting of several types of layers.

In the first stage, the input data is processed by passing the images through filters to extract important details and reduce the file size. This is achieved by creating a combination of one or more convolutional and pooling layers.

Then the processed data is flattened and becomes the input layer of the neural network.

In the next phase, we create the hidden layers of the neural network in which the input data is processed. These layers are functions with a known mathematical structure that perform certain calculations. Dropout layers, who are also functions, are added to avoid overfitting.

Finally, the structure of the output layer is defined and finished model is compiled.

## Determination of neural network parameters through testing

With different configuration of neural network layers, different speed and accuracy of data processing is achieved. The goal is to choose the appropriate number of layers of the neural network with the appropriate parameters in order to achieve the best results.
Testing will be conducted on a modified dataset of 500 images of three different types of traffic signs.

First was verified conclusion based on the experience of working with playground.tensorflow, which proved to be correct in this case as well - adding hidden layers did not significantly improve the accuracy of data processing nor did it reduce the required time, so only one hidden layer with one Dropout layer was used.

Below is a table with different parameters:

"filter" - number of filters of convolutional layers
"matrix" - dimensiond of pooling matrix
"units" - number of units (cells, nodes) of hiden layer
"accuracy()" - max accuracy for all 10 epochs, in parentheses the epoch number with 99% accuracy
"time" - time for 99% accuracy / time for all 10 epochs
"conv/pool" = number of convolution layers / pooling layers

|  accuracy(), time  |  filter  |  matrix  |  units  | dropout | conv/pool |
|  :--------------:  | :------: |  :-----: |  :---:  | :-----: | :-------: |
|    1.0(3), 10/31   |    32    |    2x2   |   256   |   0.3   |    1/1    |
|    1.0(4), 13/31   |    32    |    2x2   |   256   |   0.5   |    1/1    |
|    1.0(4), 13/31   |    32    |    2x2   |   256   |   0.7   |    1/1    |
|    1.0(3), 8/22    |    32    |    2x2   |   256   |   0.3   |    2/2    |
|    1.0(4), 10/22   |    32    |    2x2   |   256   |   0.5   |    2/2    |
|    1.0(4), 10/22   |    32    |    2x2   |   256   |   0.7   |    2/2    |


|  accuracy(), time  |  filter  |  matrix  |  units  | dropout | conv/pool |
|  :--------------:  | :------: |  :-----: |  :---:  | :-----: | :-------: |
|    1.0(3), 11/32   |    32    |    2x2   |   512   |   0.3   |    1/1    |
|    1.0(4), 14/22   |    32    |    2x2   |   512   |   0.5   |    1/1    |
|    1.0(4), 14/22   |    32    |    2x2   |   512   |   0.7   |    1/1    |
|    1.0(3), 8/22    |    32    |    2x2   |   512   |   0.3   |    2/2    |
|    1.0(3), 8/22    |    32    |    2x2   |   512   |   0.5   |    2/2    |
|    1.0(4), 10/22   |    32    |    2x2   |   512   |   0.7   |    2/2    |

By now conclusion is:
* lower dropout is better than higher
* two pairs of convulation/dropout layers are better than one
So, from now we will use 0.3 dropout and two pairs conv/pool

|  accuracy(), time  |  filter  |  matrix  |  units  |
|  :--------------:  | :------: |  :-----: |  :---:  |
|    1.0(4), 6/12    |    32    |    3x3   |   256   |
|    1.0(4), 6/12    |    32    |    3x3   |   512   |
|    1.0(4), 7/16    |    32    |    3x3   |   1024  |
|    1.0(4), 10/22   |    64    |    3x3   |   256   | 
|    1.0(4), 10/22   |    64    |    3x3   |   512   | 
|    1.0(4), 10/22   |    64    |    3x3   |   1024  | 

## Conclusion

To form the most efficient neural network for a specific task, it is necessary to harmonize the parameters of the neural network. All the tests with the used parameters had 100% accuracy in at least one epoch, but often after reaching 100% accuracy, they had worse results, which may be a consequence of overfitting, but it may also be a consequence of poor quality of some input images - there are among the images those that even the human eye can't determine which sign it is.

### Three types of traffic signs tests

* 10 epochs are too many for this test since certain parameter configurations provide over 99% accuracy even in the third epoch.

* Tests shows that 32 filters of convolutional layer are the optimal number of filters for this task.

* 0.3 dropout has the best results.

* Pooling matrix 3x3 is better than 2x2 for this purpose but 4x4 gives insufficiently accurate results.

* It seems that hidden layer with 256 units is good choice for this test but since the main test has an input of 43 different types of traffic signs and 512 units does not give worse results, for the basic test we will use a hidden layer with 512 units. We will not use more hidden layers because the data processing time increases while the accuracy shows larger oscillations.

### Hint regarding the required software for this project (for Ubuntu)

If you have older PC and your CPU doesn't support AVX then you won't be able to run newer versions of TensorFlow, you will get this error: **Illegal instruction (core dumped)**. This problem can be overcome by using older versions of TensorFlow that doesn't require AVX, but other programs also must be adapted to this change.

All this should be done in a virtual environment to avoid change of the base system configuration. It is the best to install Anaconda first as it does a great job of solving problems with library dependencie conflicts.

* First create a new virtual environment in Anaconda, select Python 2.7.18 which is the latest version that supports the required version of TensorFlow. Use listed package versions.

* $pip install opencv-python==4.2.0.32  (conda doesn't have this package)

* $conda install scikit-learn=0.20.0

* $conda install tensorflow=2.1

Now the script run from the virtual environment will work normally but still won't be able to use check50 as it requires Python3.
