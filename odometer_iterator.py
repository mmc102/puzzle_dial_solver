import numpy as np
import itertools

dial_1 = 'twtmactnwbtof'
dial_2 = 'uonihehonahai'
dial_3 = 'relisdlovttle'
dial_4 = 'nipsgcstpiuih'
dial_5 = 'taolhebggiofe'
dial_6 = 'hanwtrttmaarr'
dial_7 = 'ebzpatttwtsae'
dial_8 = 'tsehehokksyal'
dial_9 = 'apebeneearree'
dial_10 = 'bmaelidxysame'
dial_11 = 'lnoioytigaubp'
dial_12 = 'ettunuohnirso'
dial_13 = 'sgrusdnstwroh'

dials = [dial_10,dial_11, dial_12,dial_13]  #dial_1,dial_2,dial_3,dial_4,dial_5,dial_6,dial_7,dial_8 ,dial_9] 



#function to record the state of the dials with each spin
#could be made faster by only moving the dial one click at a time as opposed to back to wildtype then to next position 
def incriment(matrix,odometer):
    new_matrix = np.copy(matrix)
    new_matrix = np.transpose(new_matrix)
    matrix = np.transpose(matrix)
    
    for the_index, the_position in enumerate(odometer):
        
        new_matrix[the_index] = np.roll(matrix[the_index],the_position)
        
    new_matrix = np.transpose(new_matrix)
    matrix = np.transpose(matrix)
    new_matrix = new_matrix.tolist()
    all_matrix.write(str(new_matrix))
    all_matrix.write('\n')
    for i in new_matrix:
        print(i)
    print('---')
    
    
    
if __name__ == '__main__':
    matrix = []

    #prepare the initial matrix
    for dial in dials:
        temp_dial = []
        for letter in dial:
            temp_dial.append(letter)
        matrix.append(temp_dial)

                

    #turn to np 2d array and transpose 

    matrix = np.array(matrix)
    matrix = np.transpose(matrix)

    the_odom_choices = list(range(len(matrix)+1))
    all_matrix = open('all_matrix.txt', 'w+')
    for odom in itertools.product(the_odom_choices, repeat=len(matrix[0])):
        incriment(matrix,odom)
    all_matrix.close()