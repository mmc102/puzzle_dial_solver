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

dials_6 = [0,[dial_6,dial_7,dial_8 ,dial_9]] #[dial_10,dial_11, dial_12,dial_13]  dial_1,dial_2,dial_3,dial_4,dial_5,dial_6,dial_7,dial_8 ,dial_9] 
dials_10 = [0,[dial_10,dial_11, dial_12,dial_13]]
dials_2 = [1,[dial_2,dial_3,dial_4,dial_5,dial_6]]

first_dial = []

for i in dial_1:
    i = [i]
    first_dial.append(i)

first_dial = np.array(first_dial)


#could be made faster by only moving the dial one click at a time as opposed to back to wildtype then to next position 
#given a matrix and a list of positions this function aligns a copy of the matrix to such a position and returns it
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
    

def produce_matricies(the_dials):   #mainly using the incriment function, this function takes a list of strings that are the dials, turns them into the 
    #appropriate matrix and makes all possible combinations of the matrix. This returns all the possible matricies in a list.
    
    #prepare the initial matrix
    all_new_matricies = []
    matrix = []
    for dial in the_dials[1]:
        temp_dial = []
        for letter in dial:
            temp_dial.append(letter)
        matrix.append(temp_dial)

    #turn to np 2d array and transpose
    matrix = np.array(matrix)
    matrix = np.transpose(matrix)

    #iterate through all combination of the dials, returning each dial 
    the_odom_choices = list(range(len(matrix)+1))
    for odom in itertools.product(the_odom_choices, repeat=len(matrix[0])):
        no_first_dial_matrix = (incriment(matrix,odom)) 
        #because first dial doesnt spin, append it to the ones following that do spin
        if the_dials[0] == 1:
            appened_dial = np.append(first_dial,no_first_dial_matrix,axis =1)
            all_new_matricies.append(appened_dial)
        #these dials are either the second or third set 
        else:
            all_new_matricies.append(no_first_dial_matrix)
    return all_new_matricies   
    
    #this function looks at a flawed version of "all the words". basically, it looks at all the words assuming there can only be two words per line
    #it adds points to a score, if in that grid search it finds a word. the longer the word, the more points. The line of thinking is that in the smaller sub_matrix
    #the correct allignments will present the most words, even if they are truncated. i.e "parked" would count par, park, and parked. 
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
          
    return best_score   #returns a 2 dimensional list of one element, a score and a matirx



winner_1_5 = (score_matrix(produce_matricies(dials_2)))
winner_6_9 = (score_matrix(produce_matricies(dials_6)))
winner_10_13 = (score_matrix(produce_matricies(dials_10)))

matrix_1 = np.array(winner_1_5[1])

matrix_2 = np.array(winner_6_9[1])
matrix_2 = np.transpose(matrix_2)
matrix_2 = matrix_2[1:]
matrix_2 = np.transpose(matrix_2)


matrix_3 = np.array(winner_10_13[1])


matrix_total = np.append(matrix_1,matrix_2,axis = 1)
matrix_total = np.append(matrix_total,matrix_3,axis =1)



def rotate(matrix_spin,num_rolls,start,finish):
    matrix_spin = np.transpose(matrix_spin)
    for i in range(start,finish):
        matrix_spin[i] = np.roll(matrix_spin[i],num_rolls)
    matrix_spin = np.transpose(matrix_spin)
    return matrix_spin



def secondary_score_matrix(a_matrix):
    scoreable_words = []
    a_matrix = a_matrix.tolist()
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
                if len(i) >= 9:
                    score += 200
                elif len(i) >= 5:
                    score += 50
                elif len(i) >= 4:
                    score += 20
                else:
                    score += 10
        
    scoreable_words = []  
    score_and_matrix = [score, a_matrix]
    return score_and_matrix       
    

final_answer = [0,0]

for odom in itertools.product(range(0,14), repeat=2):
        print(odom)
        current_score = (secondary_score_matrix(rotate(rotate(matrix_total,odom[0],6,9),odom[1],9,13)))
        if current_score[0] > final_answer[0]:
            final_answer = current_score


print('the answer is:')
for x in final_answer[1]:
    print(''.join(x))
print('---')


