""" Start server for real time digit recognition with Spark module."""

import sys

from pyspark.ml.classification import MultilayerPerceptronClassificationModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from flask import Flask
from flask import request
from flask import abort
from flask import jsonify

from train import read_dataset
from spark_helper import start_spark_instance
from spark_helper import json_to_dataset


def load_model(path,  sparksession):
    """ Load the model.

    Args:
        path (string):  the path to the model.
        sparkSession (SparkSession): the spark session.

    Returns:
        the loaded model.

    """
    model = MultilayerPerceptronClassificationModel.load(path)
    return model


def start_rest_server(model,  spark):
    """ Start the rest server

    Args:
    model: the model used to answer queries.
    spark (SparkSession): the spark session

    Returns:
        the server.

    """
    app = Flask(__name__)

    @app.route('/picture', methods=['POST'])
    def evaluate_picture():
        if not request.json or not 'data' in request.json:
            abort(400)
        single_line_df = json_to_dataset(spark, request.json)
        result = model.transform(single_line_df)
        predictions = result.select('prediction').collect()[0].prediction
        return jsonify({'predictions': predictions}), 201
        
    app.run(debug=True)
    
def main(argv):
    """ Main function."""

    # start spark session
    spark = start_spark_instance()

    # Load model
    model_path = 'models/model3'
    model = load_model(model_path, spark)
    #df_test = read_dataset(spark, 'samples/mnist_test.csv')
   # result = model.transform(df_test)
    #predictions = result.select('prediction', 'label')
    #evaluator = MulticlassClassificationEvaluator(metricName='accuracy')
    #print str(evaluator.evaluate(predictions))
    
    # Start rest server
    start_rest_server(model,  spark)


if __name__ == '__main__':
    main(sys.argv[1:])
