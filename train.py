"""Real time digit recognition with Spark module."""

__version__ = '0.1'
__author__ = 'Fabien Celier'
__all__ = []

from pyspark.sql import SparkSession

from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

def useless_load():
    """ Load the datasets. """
    df_train_multicol = spark.read.format('csv').option('inferSchema','true').load('samples/mnist_train.csv').withColumnRenamed('_c0','label')
    df_train = assembler.transform(df_train_multicol).select('label','features').cache()

    df_test_multicol = spark.read.format('csv').option('inferSchema','true').load('samples/mnist_test.csv').withColumnRenamed('_c0','label')
    df_test = assembler.transform(df_test_multicol).select('label','features').cache()

def start_spark_instance():
    """ Launch spark instance """
    spark = SparkSession.builder.appName('image-recognition').config('spark.driver.memory', '8G').config('spark.executor.memory', '8G').master('local[*]').getOrCreate()
    # set log level to error
    spark.setLogLevel('ERROR') ?
    print '\tSpark session started.'
    return spark

def read_dataset(spark, path_to_csv):
    """ Read a csv dataset and format it for multilayer perceptron fastforward. 

    Arguments:
    spark -- the spark session
    path_to_csv -- the path to the csv file containing thedataset.

    Returns:
    A transformed dataset ready to train the model.
    """
    feature_cols = []
    for i in range(0,28*28):
      feature_cols.append("_c"+str(i+1))

    assembler = VectorAssembler(
    inputCols=feature_cols,
    outputCol='features')

    df = spark.read.format('csv').option('inferSchema','true').load(path_to_csv).withColumnRenamed('_c0','label')
    df = assembler.transform(df).select('label','features').cache()
    return df

def define_model(layers, max_iter, train_data):
    """ Define the trained Multilayer Perceptron model.

    Arguments:
    layers -- array representinghe layers of the perceptron, such as [784, 800, 10] fo a single hidden layer.
    max_iter -- maximum number of iterationsduring training.
    train_data -- the dataset to train the model with.
    """
    trainer = MultilayerPerceptronClassifier(maxIter=max_iter, layers=layers, blockSize=128, seed=1234)
    model = trainer.fit(train_data)
    return model

def load_train_evaluate(spark):
    """ Loads data, trains and evaluates the model.

	This can be called inside an existing spark such as Pysark.

    Arguments:
    spark -- the spark session.
    """
    print '\tLoad data'
    df_train = read_dataset(spark, 'samples/mnist_train.csv')
    df_test = read_dataset(spark, 'samples/mnist_test.csv')
    print '\tData loaded: ',str(df_train.count()), ' lines in train dataset'

    layers = [ 784, 784, 800,10]
    model = define_model(layers, 3, df_train)
    print '\tModel trained'

    result = model.transform(df_test)
    predictions = result.select('prediction','label')
    evaluator = MulticlassClassificationEvaluator(metricName='accuracy')
    print str(evaluator.evaluate(predictions))
    return model

def save_model(model, path):
    """ Save the current model

	Arguments:
    model -- The model to save
    path -- the path where to save it.
    """
    model.save(path)

def main():
    spark = start_spark_instance()
    model = load_train_evaluate(spark)
    save_model(model, 'models/model3')

if __name__ == '__main__':
    main()


