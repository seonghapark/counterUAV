package com.example.root.pubzmq;

import android.os.Handler;

import org.zeromq.ZMQ;

/**
 * Created by root on 18. 1. 12.
 */

public class ZMQPublisher implements Runnable {
    private final Handler uiThreadHandler;
    private boolean isOn;

    ZMQ.Context context;
    ZMQ.Socket socket;

    public ZMQPublisher(Handler uiThreadHandler) {
        this.uiThreadHandler = uiThreadHandler;
    }

    public void sendGraph1() {
        if(!isOn) {
            logMsg("NOT Connected...");
            return;
        }
        logMsg("Sending Graph_1");
    }

    public void turnOn() {
        if(isOn) {
            logMsg("Already Connected");
            return;
        }
        context = ZMQ.context(1);
        socket = context.socket(ZMQ.PUB);
        socket.bind("tcp://127.0.0.1:5559");
        logMsg("Connected!");
        isOn = true;
    }
    public void turnOff() {
        if(!isOn) {
            logMsg("Already Disconnected");
            return;
        }
        socket.close();
        context.term();
        logMsg("Disconnected!");

        isOn = false;
    }

    @Override
    public void run() {
        context = ZMQ.context(1);
        socket = context.socket(ZMQ.PUB);

        socket.bind("tcp://127.0.0.1:5559");

        int i = 0;
        while(!Thread.currentThread().isInterrupted()) {
            String sendTimes = NumBox.getTimes(i);
            logMsg("Sended Times" + i);
            String sendDistandces = NumBox.getDistances(i);
            logMsg("Sended Distances" + i);

            socket.send(sendTimes, 0);
            socket.send(sendDistandces, 0);
            i++;
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
        socket.close();
        context.term();
    }

    public void logMsg(String msg) {
        uiThreadHandler.sendMessage(
                Util.bundledMessage(uiThreadHandler, msg));
    }
}