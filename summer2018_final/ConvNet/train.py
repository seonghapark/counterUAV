import tensorflow as tf
from model import RadarNet
from data_input import DataLoader, label_img 

NUM_CLASSES = 4
save_model_path = ./radarnet_model_saved

def main():

    if __name__ == '__main__':
        opt = {}
        opt['batch_size'] = 5
        opt['num_class'] = NUM_CLASSES
        opt['learning_rate'] = 1e-3
        opt['dropout_p'] = 0.5
        opt['epoch'] = 10
        opt['model_path'] = save_model_path 

    tf.reset_default_graph()

    x = tf.placeholder(tf.float32, shape=(None, 30, 30, 1), name='input')
    y = tf.placeholder(tf.float32, shape=(None, 10), name='output')

    m = RadarNet(opt)
    model_out = m.model(x)
    cost = m.loss(model_out, label)
    optim = m.optimizer(cost)
    acc = m.accuracy(model_out)

    print("Training...")
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for epoch in range(opt['epoch']):
            for i in range(1, opt['batch_size'] + 1):
               for batch_features, batch_labels in DataLoader(i, batch_size):
                    m.train_neural_network(sess, optim, opt['dropout_p'], batch_features, batch_labels)
                print('Epoch {:>2}, Radar Batch {}:'.format(epoch+1, i), end='')
                m.print_stats(sess, batch_features, batch_labels, cost, acc)

        saver = tf.train.Saver()
        save_path = saver.save(sess, opt['model_path'])


if __name__ == "__main__":
    main() 
