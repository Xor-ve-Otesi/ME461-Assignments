def Toparla(L):
    '''
    note that L is an iterable object such as a list.
    your code should not crash no matter what.
    try except or whatever message you find fit.
    The function returns two things:
        -sum of all numbers that can be added 
        -a list of all things that couldn't be added. format of this list is up to you.
    '''
    sum = 0 	#defining the holder variables for holding and returning
    others = [] #the elements and sum at the end of the function
                #sum holds the sum value and others list holds the
                #list of the remaining variables
    
                                                                        #the whole function is on try-except since the function should
                                                                        #give an error if the input variable is something that cannot
                                                                        #be added to the others list
    try:
        if type(L) is list or type(L) is tuple: 						#checking the list/tuple case
            for element in L: 											#looking for each element in the list/tuple
                if type(element) is list or type(element) is tuple: 	#if the 
                    sumL, othersL = Toparla(element) 					#calling the function for the nested lists/tuples recursively
                    sum += sumL											#adding and appending the returned values from the recursive function called above
                    ''' for otherL in othersL: #if this line is used, then the returned others tuple has no nested lists/tuples inside '''
                    others.append(othersL) 								#appending the list returned from recursive call to the list on this function call
                elif type(element) is int or type(element) is float: 	#if the element is float or int, 
                    sum += element										#this element is added to the sum function
                else: 													#if the element is not a list, tuple, integer or float, 
                    others.append(element)								#adding it to the others list
            return sum, others 											#returning the summed value and the others list
                                                                        #using the same algorithm only for 1 element here
        elif type(L) is int or type(L) is float: 						#if the given variable is float or int
            sum += L													#add it to the sum value (i.e return it as sum variable)
        else: 															# if the element is not an integer or float, 
            others.append(L)											#add it to the others list (return it as others variable)
        return sum, others 												#returning the summed value and the others list

    except:
        print("Given argument is not valid.")							#printing error if the given input cannot be processed