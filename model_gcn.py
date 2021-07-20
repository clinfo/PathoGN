import tensorflow as tf
import kgcn.layers
from kgcn.default_model import DefaultModel
import tensorflow.contrib.keras as K
import numpy as np

# placeholders['label_list']= tf.placeholder(tf.int64, shape=(batch_size,None,2),name="label_list")


class GCN(DefaultModel):
    def build_placeholders(self, info, config, batch_size, **kwargs):
        # input data types (placeholders) of this neural network
        keys = ['adjs', 'nodes', 'label_list', 'node_label', 'mask', 'dropout_rate', 'enabled_node_nums', 'is_train', 'features']
        return self.get_placeholders(info, config, batch_size, keys, **kwargs)

    def build_model(self, placeholders, info, config, batch_size, **kwargs):
        adj_channel_num = info.adj_channel_num
        embedding_dim=config["embedding_dim"]
        in_adjs = placeholders["adjs"]
        features = placeholders["features"]
        in_nodes = placeholders["nodes"]
        mask = placeholders["mask"]
        labels=placeholders["node_label"]
        label_list=placeholders["label_list"]
        enabled_node_nums = placeholders["enabled_node_nums"]
        is_train = placeholders["is_train"]
        dropout_rate = placeholders["dropout_rate"]
        layer = features

        #init="glorot_uniform"
        init="he_normal"
        activate=lambda x:tf.clip_by_value(x,0,1.5)
        #layer = tf.nn.relu6(layer)
        #layer = tf.nn.sigmoid(layer)
        reg=tf.contrib.layers.l2_regularizer
        if features is None:
            layer=K.layers.Embedding(info.all_node_num,embedding_dim)(in_nodes)
        layer = activate(layer)
        layer=kgcn.layers.GraphConv(64,adj_channel_num)(layer,adj=in_adjs)
        layer=tf.nn.sigmoid(layer)
 
        #=== GIN ===
        """
        gin_block_out=[]
        layer = kgcn.layers.GINAggregate(adj_channel_num)(layer, adj=in_adjs)
        layer = kgcn.layers.GraphDense(64,kernel_regularizer=reg,kernel_initializer=init)(layer)
        layer = activate(layer)
        layer = K.layers.Dropout(dropout_rate)(layer)
        layer = kgcn.layers.GraphDense(64,kernel_regularizer=reg,kernel_initializer=init)(layer)
        layer = activate(layer)
        gin_block_out.append(layer)
        
        layer = kgcn.layers.GINAggregate(adj_channel_num)(layer, adj=in_adjs)
        layer = kgcn.layers.GraphDense(64,kernel_regularizer=reg,kernel_initializer=init)(layer)
        layer = activate(layer)
        layer = K.layers.Dropout(dropout_rate)(layer)
        """
        #========

        # layer: batch_size x graph_node_num x dim
        layer=kgcn.layers.GraphDense(info.label_dim)(layer)
        prediction=tf.nn.softmax(layer)

        pred_layer=tf.gather(layer[0,:,:],label_list[0,:,0])
        label_layer=tf.one_hot(label_list[0,:,1],2)
        w=tf.constant(info.class_weight)
        sample_weights = tf.reduce_sum(tf.multiply(label_layer, w), 1)
        cost=tf.nn.softmax_cross_entropy_with_logits(labels=label_layer,logits=pred_layer)
        # computing cost and metrics
        #cost=mask*tf.reduce_mean(cost*sample_weights,axis=1)
        #cost=mask*tf.reduce_mean(cost,axis=1)
        cost_opt=tf.reduce_mean(cost*sample_weights)

        metrics={}
        cost_sum=tf.reduce_sum(cost)
        ####

        pred=tf.gather(prediction[0,:,:],label_list[0,:,0])
        pre_count=tf.cast(tf.equal(tf.argmax(pred,1), label_list[0,:,1]),tf.float32)
        metrics["correct_count"]=tf.reduce_sum(pre_count)
        ###

        #pre_count=mask_labels*tf.cast(tf.equal(tf.argmax(prediction,2), tf.argmax(labels,2)),tf.float32)
        #correct_count=tf.reduce_sum(pre_count,axis=1)
        #metrics["correct_count"]=tf.reduce_sum(correct_count)
        #count=tf.reduce_sum(mask_labels)
        count=tf.shape(label_list[0,:,0])[0]
        metrics["count"]=count
        self.out = layer
        return self, prediction, cost_opt, cost_sum, metrics




