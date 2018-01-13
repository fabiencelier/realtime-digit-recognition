""" Tools to work with Spark. """

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.ml.feature import VectorAssembler


def assemble(df,  column_prefix):
    """ Assemble a dataset to vector.
    
    Args:
        df: the dataset to assemble.
        column_prefix (String): the prefix for column without name ( _ or _c )

    Returns:
        assembled dataset.
    
    """
    feature_cols = []
    for i in range(0, 28*28):
        feature_cols.append(column_prefix + str(i+1))
    
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol='features')
    return assembler.transform(df)


def start_spark_instance():
    """ Launch spark instance.

    Returns:
        SparkSession: the spark session
    
    TODO:
        We should read configs from a file.

    """
    spark = SparkSession.builder\
        .appName('image-recognition')\
        .config('spark.driver.memory', '8G')\
        .config('spark.executor.memory', '8G')\
        .master('local[*]')\
        .getOrCreate()
    # set log level to error
    # spark.setLogLevel('ERROR')
    print '\tSpark session started.'
    return spark


def read_dataset(spark, path_to_csv):
    """ Read a csv dataset and format it for multilayer perceptron fastforward.

    Args:
        spark (SparkSession): the spark session
        path_to_csv (string): the path to the csv file containing thedataset.

    Returns:
        A transformed dataset ready to train the model.

    """
    df = spark.read\
        .format('csv')\
        .option('inferSchema', 'true')\
        .load(path_to_csv)\
        .withColumnRenamed('_c0', 'label')
    df = assemble(df, '_c')\
        .select('label', 'features')\
        .cache()
    return df


def json_to_dataset(spark, json):
    """ Convert a JSON object to a single line dataset.

    Args: 
        spark (SparkSession): the spark session.
        json (string): the json to convert.
        

    Returns:
        A single line dataset.

    """
    
    # struct = StructType([StructField("features", ArrayType(), True)])
    row = Row(feature=json['data'])
    df = spark.createDataFrame(row)
    df = assemble(df, '_').select('features')
    return df


if __name__ == '__main__':
    line = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,84,185,159,151,60,36,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,222,254,254,254,254,241,198,198,198,198,198,198,198,198,170,52,0,0,0,0,0,0,0,0,0,0,0,0,67,114,72,114,163,227,254,225,254,254,254,250,229,254,254,140,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17,66,14,67,67,67,59,21,236,254,106,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,83,253,209,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,233,255,83,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,129,254,238,44,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,59,249,254,62,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,133,254,187,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,205,248,58,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,126,254,182,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,75,251,240,57,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,19,221,254,166,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,203,254,219,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,38,254,254,77,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,224,254,115,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,133,254,254,52,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,61,242,254,254,52,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,121,254,254,219,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,121,254,207,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    json = {'data': line }
    print json
    spark = start_spark_instance()
    df = json_to_dataset(spark, json)
    print df.select('features').collect()[0].features
