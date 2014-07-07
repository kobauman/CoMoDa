import graphlab
import numpy as np
import random

filename = '../data/txt/CoMoDa.csv'

# Load a small training set. The data is 2.8 MB.
train_data = graphlab.SFrame.read_csv(filename, column_type_hints={"rating":int})

print type(train_data)




def trainTestAccuracy(train_data, num_latent_factors = 10, regularization_parameter = 0.5):
    model = graphlab.recommender.matrix_factorization.create(train_data, user="userID", item="itemID",
                                                    target="rating", holdout_probability=0.1,
                                                    D = num_latent_factors,
                                                    reg = regularization_parameter,
                                                    verbose=False,
                                                    niter = 15,
                                                    plot=False)
    
    return model.training_stats()['validation_rmse']


def crossValidation(train_data, folds = 10):
    rmse = list()
    block_size = train_data.num_rows()/folds
    nums = range(train_data.num_rows())
    random.shuffle(nums)
    for ind in range(folds):
        train_index = [1]*train_data.num_rows()
        test_index = [0]*train_data.num_rows()
        for i in range(ind*block_size, (ind+1)*block_size):
            if i < len(train_index):
                train_index[i] = 0
                test_index[i] = 1
        train_i = graphlab.SArray(data = train_index, dtype=int)
        test_i = graphlab.SArray(data = test_index, dtype=int)
        
        train = train_data._row_selector(train_i)
        test = train_data._row_selector(test_i)
        
        
        model = graphlab.recommender.matrix_factorization.create(train_data, user="userID", item="itemID",
                                                    target="rating", holdout_probability=0.1,
                                                    D = 10,
                                                    reg = 0.05,
                                                    verbose=False,
                                                    niter = 15,
                                                    plot=False)
        
        rmse_result = model.evaluate(test,verbose=False)['rmse_overall']
        print rmse_result
        
        
        
        rmse.append(rmse_result)
        #print ind, rmse
    return np.average(rmse)

print crossValidation(train_data, )
exit()  
    
for i in range(10):
    print 'RMSE', trainTestAccuracy(train_data)

exit()
for measure in model.training_stats():
    print measure,':',model.training_stats()[measure]


query_data = training_data.head()
query_result = model.predict(query_data)

# Normalize the query results 
result_sarray = query_result['prediction']
query_result['prediction'] = (result_sarray - result_sarray.min())/(result_sarray.max() - result_sarray.min()) * query_data['rating'].max()

print query_result.head()
