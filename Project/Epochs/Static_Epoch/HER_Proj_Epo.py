import numpy
#scipy.special for the sigmoid function expit()
import scipy.special
#using below packages to load your own 28x28 .png pictures

import matplotlib.pyplot
# ensure the plots are inside this notebook, not an external window

# scipy.ndimage for rotating image arrays
import scipy.ndimage

# import NN_template
from NN_template import *

#number of input, hidden and output hnodes
input_nodes=784
hidden_nodes=100
output_nodes=10

#learning rate is 0.3
'''
while 0.1, performance = 95.41%
while 0.3, performance = 94.48%
'''
learning_rate=0.05

#create instance of neural network
n=neuralNetwork(input_nodes,hidden_nodes,output_nodes,learning_rate)

#load the mnist training data CSV file into a list
training_data_file=open("../mnist_dataset/mnist_train.csv","r")
training_data_list=training_data_file.readlines()
training_data_file.close()

#training the neural network

#epochs is the number of times the training data set is used for training
epochs=7
'''
while epochs=2, performance=95.05%
while epochs=7, performance=96.84%
'''

print("training init...\n")

# train the neural network

for e in range(epochs):
    # go through all records in the training data set
    print ("epoch %d start..."%(e+1)),
    for record in training_data_list:
        # split the record by the ',' commas
        all_values = record.split(',')
        # scale and shift the inputs
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        # create the target output values (all 0.01, except the desired label which is 0.99)
        targets = numpy.zeros(output_nodes) + 0.01
        # all_values[0] is the target label for this record
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)

        ## create rotated variations
        # rotated anticlockwise by x degrees
        inputs_plusx_img = scipy.ndimage.interpolation.rotate(inputs.reshape(28,28), 10, cval=0.01, order=1, reshape=False)
        n.train(inputs_plusx_img.reshape(784), targets)
        # rotated clockwise by x degrees
        inputs_minusx_img = scipy.ndimage.interpolation.rotate(inputs.reshape(28,28), -10, cval=0.01, order=1, reshape=False)
        n.train(inputs_minusx_img.reshape(784), targets)

        # rotated anticlockwise by 10 degrees
        #inputs_plus10_img = scipy.ndimage.interpolation.rotate(inputs.reshape(28,28), 10, cval=0.01, order=1, reshape=False)
        #n.train(inputs_plus10_img.reshape(784), targets)
        # rotated clockwise by 10 degrees
        #inputs_minus10_img = scipy.ndimage.interpolation.rotate(inputs.reshape(28,28), -10, cval=0.01, order=1, reshape=False)
        #n.train(inputs_minus10_img.reshape(784), targets)

        pass
    print ("epoch %d succeed!\n"%(e+1))
    pass

#test the neural network

# load the mnist test data CSV file into a list
test_data_file = open("../mnist_dataset/mnist_test.csv", 'r')
test_data_list = test_data_file.readlines()
test_data_file.close()

# test the neural network

#scorecard for how well the network performs,initially empty
scorecard=[]

#go through all the records in the test dataset
for record in test_data_list:
    #split the record by the "," commas
    all_values=record.split(',')
    #correct answer is the first values
    correct_label=int(all_values[0])
    print(correct_label,"correct label")
    #scale and shift the inputs
    inputs=(numpy.asfarray(all_values[1:])/255.0*0.99)+0.01
    #query the network
    outputs=n.query(inputs)
    #the index of the highest value correponds to the label
    label=numpy.argmax(outputs)
    print(label,"network's answer")
    #append correct or incorrect to list
    if(label==correct_label):
        #network's answer matches correct answer, add 1 to scorecard
        scorecard.append(1)
    else:
        #network's answer doesn't match correct answer, add 0 to scorecard
        scorecard.append(0)
        pass
    pass
print(scorecard)

#calculate the performance score,the fraction of correct answer

scorecard_array=numpy.asfarray(scorecard)
print("performance = ",scorecard_array.sum()/scorecard_array.size)
# run the network backwards, given a label, see what image it produces

n.save("../mode_para/7_epochs/wih.npy", "../mode_para/7_epochs/who.npy")

# label to test

for label in range(10):
    matplotlib.pyplot.subplot(3,4,label+1)
    # create the output signals for this label
    targets = numpy.zeros(output_nodes) + 0.01
    # all_values[0] is the target label for this record
    targets[label] = 0.99
    print(targets)

    # get image data
    image_data = n.backquery(targets)

    # plot image data
    matplotlib.pyplot.imshow(image_data.reshape(28,28), cmap='Greys', interpolation='None')
    matplotlib.pyplot.savefig("../picture/back_1_1_7")
matplotlib.pyplot.show()














#end