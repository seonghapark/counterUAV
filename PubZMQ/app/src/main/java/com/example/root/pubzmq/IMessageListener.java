package com.example.root.pubzmq;

/**
 * Created by root on 18. 1. 12.
 */

public interface IMessageListener {
    void messageReceived(String messageBody);
}
