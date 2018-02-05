package kr.ac.cnu.counteruav;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;

/**
 * Created by hwangtaewook on 18. 1. 11.
 */

public class Util {
    public static final String MESSAGE_PAYLOAD_KEY = "jeromq-service-payload";

    public static String reverseInPlace(byte[] input) {
        char[] string = new char[input.length];
        for (int i = 0; i < input.length; i++) {
            string[input.length - i - 1] = (char)input[i];
        }

        return String.valueOf(string);
    }

    public static void prepareMessage(Message m, String msg) {
        Bundle b = new Bundle();
        b.putString(MESSAGE_PAYLOAD_KEY, msg);
        m.setData(b);
    }

    public static Message bundledMessage(Handler uiThreadHandler, String msg) {
        Message m = uiThreadHandler.obtainMessage();
        prepareMessage(m, msg);

        return m;
    }
}
