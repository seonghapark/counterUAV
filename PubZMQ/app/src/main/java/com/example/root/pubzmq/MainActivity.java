package com.example.root.pubzmq;


import android.support.v7.app.AppCompatActivity;

import android.os.Bundle;

import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.ListView;
import android.widget.ToggleButton;


import org.zeromq.ZMQ;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity {

    private ZMQPublisher zmqPub;

    private TextView logTV;
    private EditText sendET;

    private static final DateFormat DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd'T'HH:mmZ");

    private static String getTimeString() {
        return DATE_FORMAT.format(new Date());
    }

    private void serverMessageReceived(String messageBody) {
        logTV.append(getTimeString() + " - server published: " + messageBody + "\n");
        scrollBottom(logTV);
    }

    private final MessageListenerHandler serverMessageHandler = new MessageListenerHandler(
            new IMessageListener() {
                @Override
                public void messageReceived(String messageBody) {
                    serverMessageReceived(messageBody);
                }
            }, Util.MESSAGE_PAYLOAD_KEY);

    private void scrollBottom(TextView textView) {
        int lineTop =  textView.getLayout().getLineTop(textView.getLineCount());
        int scrollY = lineTop - textView.getHeight();
        if (scrollY > 0) {
            textView.scrollTo(0, scrollY);
        } else {
            textView.scrollTo(0, 0);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        logTV = (TextView)findViewById(R.id.logTV);
        logTV.setMovementMethod(new ScrollingMovementMethod());
        sendET = (EditText)findViewById(R.id.sendET);

        new Thread(new ZMQPublisher(serverMessageHandler)).start();

        findViewById(R.id.sendBtn).setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {

                    }
                });


        findViewById(R.id.sendGraphBtn1).setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        zmqPub.sendGraph1();
                    }
                }
        );

        findViewById(R.id.onBtn).setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        zmqPub.turnOn();
                    }
                }
        );

        findViewById(R.id.offBtn).setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        zmqPub.turnOff();
                    }
                }
        );

    }
}
