import numpy as np
import itertools

dictionary = {}
def checkKey(dict, key): 
      
    if key in dict: 
        return True
    else: 
        return False
words = []


with open("google-10000-english-usa-no-swears.txt") as word_file:    
    for word in word_file:
        if len(word)>=4:
            words.append(word.strip('\n'))

for i in words:
    dictionary.update({i:''})

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

dials = [dial_6,dial_7,dial_8 ,dial_9] #[dial_10,dial_11, dial_12,dial_13]  dial_1,dial_2,dial_3,dial_4,dial_5,dial_6,dial_7,dial_8 ,dial_9] 
dials_2 = [dial_10,dial_11, dial_12,dial_13]


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
    return new_matrix 
    
def produce_matricies(the_dials):
    
    #prepare the initial matrix
    all_new_matricies = []
    matrix = []
    for dial in the_dials:
        temp_dial = []
        for letter in dial:
            temp_dial.append(letter)
        matrix.append(temp_dial)

    #turn to np 2d array and transpose
    matrix = np.array(matrix)
    matrix = np.transpose(matrix)

    #iterate through all combination of the dials, returning each dial 
    the_odom_choices = list(range(len(matrix)+1))
    all_matrix = open('all_matrix.txt', 'w+')
    for odom in itertools.product(the_odom_choices, repeat=len(matrix[0])):
       all_new_matricies.append(incriment(matrix,odom)) 
    return(all_new_matricies)  #either need to append to a list or store in a file for further use down stream 
    
def score_matrix(all_matricies):
    scoreable_words = []
    best_score = [0,0]
    for a_matrix in all_matricies:
        for i in a_matrix:
            
            i = ''.join(i)
            length = len(i)
            while length > 0:
                    word_1 = i[:length]
                    word_2 = i[length:]
                    scoreable_words.append(word_1)
                    scoreable_words.append(word_2)
                    length -=1
        score = 0
        for i in scoreable_words:
                if checkKey(dictionary,i):
                    if len(i) >= 4:
                        score += 30
                    else:
                        score += 10
            
        if score > best_score[0]:
            best_score = [score,a_matrix]
        scoreable_words = []         
          
    return best_score

winner = (score_matrix(produce_matricies(dials)))
winner_2 = (score_matrix(produce_matricies(dials_2)))
print('---')
print(winner)

print('---')

print(winner_2)