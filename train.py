"""Train model for real time digit recognition with Spark module."""

import sys
import getopt

from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from spark_helper import start_spark_instance
from spark_helper import read_dataset

__version__ = '0.1'
__author__ = 'Fabien Celier'
__all__ = []


def define_model(layers, max_iter, train_data):
    """ Define the trained Multilayer Perceptron model.

    Args:
        layers: array representing the layers of the perceptron,
            such as [784, 800, 10] for a single hidden layer.
        max_iter: maximum number of iterationsduring training.
        train_data: the dataset to train the model with.

    Returns:
        the trained model

    """
    trainer = MultilayerPerceptronClassifier(
        maxIter=max_iter,
        layers=layers,
        blockSize=128,
        seed=1234)
    model = trainer.fit(train_data)
    return model


def load_train_evaluate(spark,  iter):
    """ Load data, train and evaluate the model.

    This can be called inside an existing spark such as Pysark.

    Args:
        spark (SparkSession): the spark session.
        iter (int): the number of iteration for the training.

    Returns:
        the trained model.

    """
    print '\tLoad data'
    df_train = read_dataset(spark, 'samples/mnist_train.csv')
    df_test = read_dataset(spark, 'samples/mnist_test.csv')
    print '\tData loaded: ', str(df_train.count()), ' lines in train dataset'

    layers = [784, 784, 800, 10]
    model = define_model(layers, iter, df_train)
    print '\tModel trained'

    result = model.transform(df_test)
    predictions = result.select('prediction', 'label')
    evaluator = MulticlassClassificationEvaluator(metricName='accuracy')
    print str(evaluator.evaluate(predictions))
    return model


def save_model(model, path):
    """ Save the current model.

    Args:
        model: The model to save
        path (string): the path where to save it.

    """
    model.save(path)


def main(argv):
    """ Train and save the model.
   
  TODO:
        Use arguments.

    """

    try:
        opts, args = getopt.getopt(argv, 'htsl', ['help', 'train', 'server'])
    except getopt.GetoptError:
        sys.exit(2)
    spark = start_spark_instance()
    model = load_train_evaluate(spark,  100)
    save_model(model, 'models/modelX')


if __name__ == '__main__':
    main(sys.argv[1:])
