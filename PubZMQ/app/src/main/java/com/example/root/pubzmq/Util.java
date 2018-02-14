package com.example.root.pubzmq;
import android.os.Handler;
import android.os.Bundle;
import android.os.Message;

/**
 * Created by root on 18. 1. 12.
 */

public class Util {
    public static final String MESSAGE_PAYLOAD_KEY = "jeromq-service-payload";

    public static Message bundledMessage(Handler uiThreadHandler, String msg) {
        Message m = uiThreadHandler.obtainMessage();
        prepareMessage(m, msg);
        return m;
    }

    public static void prepareMessage(Message m, String msg) {
        Bundle b = new Bundle();
        b.putString(MESSAGE_PAYLOAD_KEY, msg);
        m.setData(b);
        return;
    }
}
