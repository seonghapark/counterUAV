package kr.ac.cnu.counteruav;

import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import static android.os.StrictMode.setThreadPolicy;

public class MainActivity extends AppCompatActivity {
    private TextView textView;
    private EditText editText;
    private ListView radar_listView;
    private radarItemAdapter radarItemAdapter;
    private ArrayList<radarItem> radarItems;

    private static final DateFormat DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd'T'HH:mmZ");

    private static String getTimeString() {
        return DATE_FORMAT.format(new Date());
    }

    private void serverMessageReceived(String messageBody) {
        radarItems.add(new radarItem(getTimeString() + " - server received: " + messageBody + "\n"));
        radarItemAdapter.notifyDataSetChanged();
    }

    private void clientMessageReceived(String messageBody) {
        radarItems.add(new radarItem(getTimeString() + " - client received: " + messageBody + "\n"));
        radarItemAdapter.notifyDataSetChanged();
    }

    private final MessageListenerHandler serverMessageHandler = new MessageListenerHandler(
            new IMessageListener() {
                @Override
                public void messageReceived(String messageBody) {
                    serverMessageReceived(messageBody);
                }
            },
            Util.MESSAGE_PAYLOAD_KEY
    );

    private final MessageListenerHandler clientMessageHandler = new MessageListenerHandler(
            new IMessageListener() {
                @Override
                public void messageReceived(String messageBody) {
                    clientMessageReceived(messageBody);
                }
            },
            Util.MESSAGE_PAYLOAD_KEY
    );

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        radar_listView = findViewById(R.id.radar_listView);
        radarItems = new ArrayList<>();
        radarItemAdapter = new radarItemAdapter(MainActivity.this, radarItems);
        radar_listView.setAdapter(radarItemAdapter);

        editText = findViewById(R.id.editText);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        setThreadPolicy(policy);

        new Thread(new ZeroMQServer(serverMessageHandler)).start();

        findViewById(R.id.send_message_button).setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        new ZeroMQMessageTask(clientMessageHandler).execute(getTaskInput());
                    }

                    protected String getTaskInput() {
                        return editText.getText().toString();
                    }
                }
        );
    }
}
