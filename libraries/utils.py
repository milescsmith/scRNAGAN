import tensorflow as tf
import numpy as np
from libraries.input_data import Scaling

def close_session(sess):
    tf.reset_default_graph()
    sess.close()

def sample_z(m, n):
    return np.random.normal(0,1, size=[m, n])

def cross_entropy(logit, y):
    return -tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logit, labels=y))

def check_scaling(s):
    if s in Scaling.__members__.keys():
        return s
    else:
        raise NotImplementedError("No such scaling method implemented")

def check_activation_function(s):
    if(s in ['sigmoid', 'leaky_relu', 'relu', 'none']):
        return s
    else:
        raise NotImplementedError("No such activation function exists")

class objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

def get_activation(s, alpha=0.1):
    if(s == 'leaky_relu'):
        return lambda x : tf.maximum(x, alpha * x)
    elif(s == 'relu'):
        return tf.nn.relu
    elif(s == 'tanh'):
        return tf.nn.tanh
    elif(s == 'sigmoid'):
        return tf.nn.sigmoid
    elif(s == 'none'):
        return None
    else:
        raise NotImplementedError("No such activation is implemented")

def leaky_relu(x, alpha=0.1):
    return tf.maximum(x, alpha * x)

def get_optimizer(name):
    if name == 'Adadelta':
        return tf.train.AdadeltaOptimizer
    elif name == 'Adagrad':
        return tf.train.AdagradOptimizer
    elif name == 'RMSProp':
        return tf.train.RMSPropOptimizer
    elif name == 'GradientDescent':
        return tf.train.GradientDescentOptimizer
    elif name == 'Adam':
        return tf.train.AdamOptimizer
    elif name == 'Ftrl':
        return tf.train.FtrlOptimizer
    else:
        raise NotImplementedError()

def get_learning_schedule(name):
    if name == 'no_schedule':
        return lambda eta0, n : eta0
    elif name == 'search_then_converge':
        return lambda eta0, n: tf.divide(eta0, (tf.add(tf.convert_to_tensor(1.0, tf.float64), tf.divide(n, tf.convert_to_tensor(1000, np.int32)))))

	#return lambda eta0, n: eta0 / (1 + n / 1000)
    else:
        raise NotImplementedError()
