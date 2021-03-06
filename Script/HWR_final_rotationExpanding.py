import numpy
#scipy.special for the sigmoid function expit()
import scipy.special
#using below packages to load your own 28x28 .png pictures

import matplotlib.pyplot
# ensure the plots are inside this notebook, not an external window

# scipy.ndimage for rotating image arrays
import scipy.ndimage

#neural network class definition
class neuralNetwork:
    #initialise the neural network
    def __init__(self,inputnodes,hiddennodes,outputnodes,learningrate):
        #set nummber of nodes in each input,hidden,output layer
        self.inodes=inputnodes
        self.hnodes=hiddennodes
        self.onodes=outputnodes

        #link weight matrices, wih and who
        #weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        #w11 w21
        #w12 w22 etc
        self.wih=numpy.random.normal(0.0,pow(self.hnodes,-0.5),(self.hnodes,self.inodes))
        self.who=numpy.random.normal(0.0,pow(self.onodes,-0.5),(self.onodes,self.hnodes))

        #learning learningrate
        self.lr=learningrate

        #activation function is the sigmoid function
        self.activation_function=lambda x:scipy.special.expit(x)
        self.inverse_activation_function = lambda x: scipy.special.logit(x)

        pass

    #train the neuralNetwork
    def train(self,inputs_list,targets_list):
        #convert inputs list to 2d arrays
        inputs=numpy.array(inputs_list,ndmin=2).T
        targets=numpy.array(targets_list,ndmin=2).T

        #calculate signals into hidden layer
        hidden_inputs=numpy.dot(self.wih,inputs)
        #calculate the signals emerging from hidden layer
        hidden_outputs=self.activation_function(hidden_inputs)

        #calculate signals into final output layer
        final_inputs=numpy.dot(self.who,hidden_outputs)
        #calculate the signals emerging from final output layer
        final_outputs=self.activation_function(final_inputs)

        #output layer error is the (target-actual)
        output_errors=targets-final_outputs
        #hidden layer error is the output_errors,split by weights, recombined at hidden nodes
        hidden_errors=numpy.dot(self.who.T,output_errors)

        #update the weights for the links between the hidden and output layers
        self.who+=self.lr*numpy.dot((output_errors*final_outputs*(1.0-final_outputs)),numpy.transpose(hidden_outputs))
        #update the weights for the links between the input and hidden layers
        self.wih+=self.lr*numpy.dot((hidden_errors*hidden_outputs*(1.0-hidden_outputs)),numpy.transpose(inputs))
        pass

    #query the neural network
    def query(self,inputs_list):
        #convert inputs list to 2d arrays
        inputs=numpy.array(inputs_list,ndmin=2).T

        #calculate signals into hidden layers
        hidden_inputs=numpy.dot(self.wih,inputs)
        #calculate the signals emerging from hidden layers
        hidden_outputs=self.activation_function(hidden_inputs)

        #calculate signals into final output layers
        final_inputs=numpy.dot(self.who,hidden_outputs)
        #calculate the signals emerging from final output layers
        final_outputs=self.activation_function(final_inputs)

        return final_outputs

    def backquery(self, targets_list):
        # transpose the targets list to a vertical array
        final_outputs = numpy.array(targets_list, ndmin=2).T

        # calculate the signal into the final output layer
        final_inputs = self.inverse_activation_function(final_outputs)

        # calculate the signal out of the hidden layer
        hidden_outputs = numpy.dot(self.who.T, final_inputs)
        # scale them back to 0.01 to .99
        hidden_outputs -= numpy.min(hidden_outputs)
        hidden_outputs /= numpy.max(hidden_outputs)
        hidden_outputs *= 0.98
        hidden_outputs += 0.01

        # calculate the signal into the hidden layer
        hidden_inputs = self.inverse_activation_function(hidden_outputs)

        # calculate the signal out of the input layer
        inputs = numpy.dot(self.wih.T, hidden_inputs)
        # scale them back to 0.01 to .99
        inputs -= numpy.min(inputs)
        inputs /= numpy.max(inputs)
        inputs *= 0.98
        inputs += 0.01

        return inputs

#number of input, hidden and output hnodes
input_nodes=784
hidden_nodes=100
output_nodes=10

#learning rate is 0.3
'''
while 0.1, performance = 95.41%
while 0.3, performance = 94.48%
'''
learning_rate=0.1

#create instance of neural network
n=neuralNetwork(input_nodes,hidden_nodes,output_nodes,learning_rate)

#load the mnist training data CSV file into a list
training_data_file=open("/mnist_dataset/mnist_train_100.csv","r")
training_data_list=training_data_file.readlines()
training_data_file.close()

#training the neural network

#epochs is the number of times the training data set is used for training
epochs=10
'''
while epochs=2, performance=95.05%
while epochs=7, performance=96.84%
'''

# train the neural network

for e in range(epochs):
    # go through all records in the training data set
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
    pass

#test the neural network

# load the mnist test data CSV file into a list
test_data_file = open("/mnist_dataset/mnist_test.csv", 'r')
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
matplotlib.pyplot.show()













#end
